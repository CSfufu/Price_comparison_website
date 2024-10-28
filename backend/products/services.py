# utils.py 或 services.py

from .models import Product, ProductPriceHistory
import logging
import requests
import json
import re
from datetime import datetime
import time
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = logging.getLogger(__name__)

def fetch_price_history_from_url(item_url):
    """
    根据商品链接获取历史价格数据。

    参数：
    - item_url: 商品的网页链接。

    返回：
    - data: 包含商品信息和历史价格数据的字典。
    """
    encoded_url = encode_url(item_url)
    api_url = 'https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'

    headers = {
        'Host': 'apapia.manmanbuy.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 mmbWebBrowse',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
    }

    post_data = {
        'methodName': 'getBiJiaInfo_wxsmall',
        'jgzspic': 'no',
        'bj': 'false',
        'p_url': encoded_url,
        't': str(int(time.time() * 1000)),  # 时间戳
    }

    try:
        response = requests.post(api_url, data=post_data, headers=headers, verify=False)
        response_text = response.text

        # 移除 JSONP 回调函数包装
        json_str = response_text.strip('?()')
        data = json.loads(json_str)

        if 'single' not in data:
            logger.error(f"无法获取商品的历史价格数据。")
            return None

        # 获取商品信息
        single_data = data['single']
        title = single_data.get('title', '未知商品')
        link = single_data.get('url', item_url)
        image_url = single_data.get('smallpic', '')

        # 解析历史价格数据
        price_history_str = single_data.get('jiagequshi', '')
        if not price_history_str:
            logger.error(f"商品的历史价格数据为空。")
            return None

        date_list, price_list = parse_price_history(price_history_str)

        # 整理数据
        result = {
            'name': title,
            'link': link,
            'image_url': image_url,
            'price_history': [
                {'date': date, 'price': price}
                for date, price in zip(date_list, price_list)
            ]
        }

        logger.info(f"成功获取商品的历史价格数据。")
        return result

    except Exception as e:
        logger.error(f"获取商品的历史价格数据时发生错误：{e}")
        return None


def fetch_price_history(product):
    """
    获取指定商品的历史价格，并保存到数据库中。

    参数：
    - product: Product 模型的实例。
    """
    item_url = product.link
    encoded_url = encode_url(item_url)
    api_url = 'https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'

    headers = {
        'Host': 'apapia.manmanbuy.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 mmbWebBrowse',
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
    }

    post_data = {
        'methodName': 'getBiJiaInfo_wxsmall',
        'jgzspic': 'no',
        'bj': 'false',
        'p_url': encoded_url,
        # 其他必要的参数...
    }

    try:
        response = requests.post(api_url, data=post_data, headers=headers, verify=False)
        response_text = response.text

        # 移除 JSONP 回调函数包装
        json_str = response_text.strip('?()')
        data = json.loads(json_str)

        if 'single' not in data:
            logger.error(f"无法获取商品 {product.name} 的历史价格数据。")
            return False

        # 解析历史价格数据
        price_history_str = data['single'].get('jiagequshi', '')
        if not price_history_str:
            logger.error(f"商品 {product.name} 的历史价格数据为空。")
            return False

        date_list, price_list = parse_price_history(price_history_str)

        # 保存数据到数据库
        for date, price in zip(date_list, price_list):
            ProductPriceHistory.objects.update_or_create(
                product=product,
                date=date,
                defaults={'price': price}
            )

        logger.info(f"成功获取并保存商品 {product.name} 的历史价格数据。")
        return True

    except Exception as e:
        logger.error(f"获取商品 {product.name} 的历史价格数据时发生错误：{e}")
        return False

# services.py

def encode_url(text):
    escape_dict = {
        '/': '%252F',
        '?': '%253F',
        '=': '%253D',
        ':': '%253A',
        '&': '%26',
    }
    # print(text, "text is here")
    new_string = ''
    for char in text:
        try:
            new_string += escape_dict[char]
        except KeyError:
            new_string += char
    # print(new_string, "new_string is here")
    return new_string


def parse_price_history(jiagequshi_str):
        """
        解析慢慢买返回的价格趋势字符串，获取日期和价格列表。
        """
        date_list = []
        price_list = []
        logger.debug(f"原始价格趋势字符串: {jiagequshi_str}")

        # 正则表达式匹配每个数据点
        pattern = r'Date\.UTC\((\d+),(\d+),(\d+)\),([\d\.]+)'
        matches = re.findall(pattern, jiagequshi_str)

        for match in matches:
            year_str, month_str, day_str, price_str = match
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)
            price = float(price_str)

            # 调整年份和月份
            adjusted_year = year + month // 12
            adjusted_month = month % 12 + 1  # 将月份转换为 1-12

            try:
                date_obj = datetime(adjusted_year, adjusted_month, day)
                date_list.append(date_obj.strftime('%Y-%m-%d'))
                price_list.append(price)
                logger.debug(f"解析成功: 日期 {date_obj.strftime('%Y-%m-%d')}, 价格 {price}")
            except ValueError as ve:
                logger.error(f"解析日期时发生错误: 年={adjusted_year}, 月={adjusted_month}, 日={day}, 错误信息: {ve}")
                continue  # 跳过无法解析的记录

        return date_list, price_list