import re
from bs4 import BeautifulSoup
import requests  # 使用 requests 进行同步请求
from urllib.parse import quote
from lib.logger import logger
from ..models import Product
from typing import List, Tuple


JD_SEARCH_URL = 'https://search.jd.com/Search'
JD_COMMON_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}


def jd_request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 30) -> dict:
    """
    请求京东获取搜索信息
    """
    results = []
    page_size = 30
    start_page = int(offset / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    keyword = quote(keyword)
    total = 0

    # 同步循环获取每一页的数据
    for page_it in range(start_page, end_page + 1):
        page = page_it * 2 - 1
        data, _total = jd_fetch_page(keyword, page, cookie)
        if _total != 0:
            total = _total
        results.extend(data)

    # 保存商品数据到数据库，并返回带有id的数据
    saved_products = save_jd_products(results)

    # 返回分页后的数据
    ret = {"results": saved_products[(offset % page_size):(offset % page_size + limit)], "total": total}

    print("京东搜索结果：")
    print(ret)

    return ret


def jd_fetch_page(keyword: str, page: int, cookie: str) -> Tuple[list, int]:
    """
    获取京东单页搜索结果
    """
    query = f'?keyword={keyword}&page={page}'
    url = f'{JD_SEARCH_URL}{query}'
    headers = {'cookie': cookie}
    headers.update(JD_COMMON_HEADERS)

    try:
        logger.info(f'request url: {url}')
        resp = requests.get(url, headers=headers)
        logger.info(f'response url: {url}, body length: {len(resp.text)}')
        ret, total = jd_parse_search_html(resp.text)
        return ret, total
    except Exception as e:
        logger.error(f"failed to request {url}, error: {e}")
        return [], 0


def jd_parse_search_html(html: str) -> Tuple[list, int]:
    """
    解析京东搜索结果的HTML
    """
    soup = BeautifulSoup(html, "html.parser")
    datalist = []

    # 提取搜索结果总数
    try:
        src = soup.head.find_all("script")[-1].text.replace("\n", '').replace("\t", '').replace('\\\'', '\'')
        total = int(re.search(r"result_count:'(\d+)'", src).group(1))
    except Exception as e:
        logger.error(f"Failed to parse total result count, error: {e}")
        total = 0

    # 解析商品信息
    for item in soup.find_all("li", class_="gl-item"):
        try:
            # 提取 SKU
            sku = item.get('data-sku', '')
            if not sku:
                logger.warning("SKU not found for an item.")
                continue  # 如果找不到 SKU，跳过该商品

            imgSrc = "https:" + item.find("div", class_="p-img").find("img")['data-lazy-img']
            price = item.find("div", class_="p-price").find("i").text

            # 检查价格是否包含问号
            if '?' in price:
                logger.warning(f"Price contains '?', skipping product SKU: {sku}")
                continue  # 跳过此商品

            info = {
                "title": item.find("div", class_="p-name p-name-type-2").find("em").text.replace(r"\t", '').replace(
                    r'\n', ''),
                "link": "https:" + item.find("div", class_="p-name p-name-type-2").find("a")["href"]
            }
            tag = item.find("div", class_="p-name p-name-type-2").find("em").find("span").text if item.find("div",
                                                                                                            class_="p-name p-name-type-2").find(
                "em").find("span") else ''
            store = {
                "title": item.find("div", class_="p-shop").find("span").text,
                "link": "https:" + item.find("div", class_="p-shop").find("span").find("a")["href"]
            }
            supply = [child.text.replace('\t', '').replace('\n', '') for child in item.find("div", class_="p-icons") if
                      child.text.strip()]
            data = {
                "sku": sku,
                "imgSrc": imgSrc,
                "price": price,
                "info": info,
                "tag": tag,
                "store": store,
                "supply": supply,
            }
            datalist.append(data)
        except Exception as e:
            logger.error(f"Failed to parse item, error: {e}")

    return datalist, total


def save_jd_products(products):
    saved_products = []
    for item in products:
        try:
            # 创建或更新商品信息
            product, created = Product.objects.update_or_create(
                product_id=item['sku'],  # 使用商品的 SKU 作为唯一标识
                platform='京东',
                defaults={
                    'name': item['info']['title'],
                    'price': item['price'],
                    'link': item['info']['link'],
                    'image_url': item['imgSrc'],
                    'store_name': item['store']['title'],
                    'store_link': item['store']['link'],
                }
            )
            # 添加数据库中的 product id 到返回数据中
            item_with_id = {**item, 'id': product.id}
            saved_products.append(item_with_id)
        except Exception as e:
            logger.error(f"Error saving JD product: {e}")

    return saved_products