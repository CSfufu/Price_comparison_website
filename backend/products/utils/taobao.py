import time
import hashlib
from urllib.parse import quote

import certifi
from lib.logger import logger
import requests  # 使用 requests 进行同步请求
import json
import re
from ..models import Product
from bs4 import BeautifulSoup  # 用于解析商品标题中的 HTML 标签
from typing import List, Tuple


TB_HOST = 'https://h5api.m.taobao.com'
TB_COMMON_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://s.taobao.com/search',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}
APPKEY = '12574478'


def sign(token, tme, appKey, data):
    st = f"{token}&{tme}&{appKey}&{data}"
    return hashlib.md5(st.encode('utf-8')).hexdigest()


def get_token(cookie):
    get_cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    _m_h5_tk = get_cookies.get('_m_h5_tk', '')
    token = _m_h5_tk.split('_')[0]
    return token


def tb_request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 48) -> dict:
    """
    请求淘宝获取搜索信息
    """
    results = []
    page_size = 48
    start_page = int(offset / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    total = 0

    # 同步循环获取每一页的数据
    for page in range(start_page, end_page + 1):
        data = tb_fetch_page(keyword, cookie, page)
        items = data.get('itemsArray', [])
        results.extend(items)
        total = data.get('mainInfo', {}).get('totalResults', 0)

    # 保存商品数据到数据库，并返回带有id的数据
    saved_products = save_tb_products(results)

    # 截取需要的结果
    ret = {'total': int(total) if isinstance(total, str) and total.isdigit() else 0, 'results': saved_products[(offset % page_size):(offset % page_size + limit)]}

    print("淘宝搜索结果：")
    print(ret)

    return ret


def tb_fetch_page(keyword: str, cookie: str, page: int) -> dict:
    """
    获取淘宝单页搜索结果
    """
    headers = {'cookie': cookie}
    headers.update(TB_COMMON_HEADERS)
    search_query = tb_pack_search_query(cookie, keyword, page)
    url = f'{TB_HOST}/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/{search_query}'

    try:
        logger.info(f'request url: {url}')
        resp = requests.get(url, headers=headers)
        logger.info(f'response url: {url}, body: {resp.text}')

        # 使用正则表达式移除 JSONP 包装，并解析 JSON 数据
        res_str = re.sub(r'^\s*callback\(|\);?\s*$', '', resp.text)
        res = json.loads(res_str)
        items = res.get('data', {}).get('itemsArray', [])

        # 过滤价格包含问号的商品
        filtered_items = []
        for item in items:
            price_info = item.get('priceShow', {})
            price = price_info.get('price', item.get('price', '0.00'))

            if '?' in price:
                logger.warning(f"Price contains '?', skipping product ID: {item.get('item_id')}")
                continue  # 跳过此商品

            filtered_items.append(item)

        # 返回过滤后的结果
        return {"itemsArray": filtered_items, "mainInfo": res.get('data', {}).get('mainInfo', {})}

    except json.JSONDecodeError as json_err:
        logger.error(f"JSON解析失败，可能是返回格式问题: {json_err}")
        return {}
    except Exception as e:
        logger.error(f"failed to request {url}, error: {e}")
        return {}


def tb_pack_search_query(cookie, keyword, page):
    """
    打包淘宝搜索请求参数
    """
    quote_keyword = quote(keyword, 'utf-8')
    str_data = f'{{"appId":"34385","params":"{{\\"page\\":{page},\\"q\\":\\"{quote_keyword}\\",\\"n\\":48}}"}}'
    quote_data = quote(str_data, 'utf-8')
    timestamp = str(time.time()).replace('.', '')[0:13]
    token = get_token(cookie)
    sgn = sign(token, timestamp, APPKEY, str_data)
    return f'?jsv=2.7.2&appKey={APPKEY}&t={timestamp}&sign={sgn}&api=mtop.relationrecommend.wirelessrecommend.recommend&v=2.0&type=jsonp&data={quote_data}'


def save_tb_products(products):
    saved_products = []
    for item in products:
        try:
            # 提取商品的 item_id，作为唯一标识符
            item_id = item.get('item_id')
            if not item_id:
                logger.warning("Item ID not found in item.")
                continue  # 如果没有 item_id，跳过该商品

            # 提取商品价格
            price_info = item.get('priceShow', {})
            price = price_info.get('price', item.get('price', '0.00'))

            # 提取商品标题，移除 HTML 标签
            title_html = item.get('title', '')
            title = BeautifulSoup(title_html, 'html.parser').get_text()

            # 提取商品链接
            auction_url = item.get('auctionURL', '')
            link = 'https:' + auction_url if auction_url.startswith('//') else auction_url

            # 提取商品图片链接
            pic_path = item.get('pic_path', '')
            image_url = 'https:' + pic_path if pic_path.startswith('//') else pic_path

            # 提取店铺信息
            shop_info = item.get('shopInfo', {})
            store_name = shop_info.get('title', '')
            shop_url = shop_info.get('url', '')
            store_link = 'https:' + shop_url if shop_url.startswith('//') else shop_url

            # 创建或更新商品信息
            product, created = Product.objects.update_or_create(
                product_id=item_id,
                platform='淘宝',
                defaults={
                    'name': title,
                    'price': price,
                    'link': link,
                    'image_url': image_url,
                    'store_name': store_name,
                    'store_link': store_link,
                }
            )
            # 添加数据库中的 product id 到返回数据中
            item_with_id = {**item, 'id': product.id}
            saved_products.append(item_with_id)
        except Exception as e:
            logger.error(f"Error saving TB product: {e}")

    return saved_products
