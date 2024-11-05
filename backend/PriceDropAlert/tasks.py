# PriceDropAlert/tasks.py
from celery import shared_task
from .models import PriceDropAlert
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
import re
import datetime
import time
import pandas as pd
from django.template.loader import render_to_string


@shared_task
def check_price_drops():
    print("Price drop check started")
    alerts = PriceDropAlert.objects.filter(active=True)
    print(alerts.count())
    for alert in alerts:
        print(f"Checking price for product: {alert.product.name}")
        product = alert.product
        latest_price = get_latest_price(product.link)
        print(latest_price, type(latest_price))

        if latest_price is not None and latest_price <= alert.target_price:
            #if latest_price is not None and latest_price <= 4000: # 用于测试
            print(f"Price dropped for {product.name}, sending email to {alert.email}")
            send_price_drop_email(alert.email, product.name, latest_price, product.link)
            # 更新提醒状态
            alert.active = False  # 停用提醒
            alert.save()

def raw(text):  # 转化URL字符串
    escape_dict = {
        '/': '%252F',
        '?': '%253F',
        '=': '%253D',
        ':': '%253A',
        '&': '%26',
    }
    new_string = ''
    for char in text:
        new_string += escape_dict.get(char, char)
    return new_string


def get_latest_price(product_link):
    try:
        # 使用您的脚本逻辑获取最新价格
        item = product_link  # 商品链接
        item_encoded = raw(item)
        url = 'https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'
        headers = {
            'Host': 'apapia.manmanbuy.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Proxy-Connection': 'close',
            'Cookie': 'ASP.NET_SessionId=uwhkmhd023ce0yx22jag2e0o;',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 mmbWebBrowse',
            'Accept-Encoding': 'gzip',
            'Connection': 'close',
        }
        postdata = 'c_devid=2C5039AF-99D0-4800-BC36-DEB3654D202C&username=&qs=true&c_engver=1.5.0&c_devtoken=&c_devmodel=iPhone%20SE&c_contype=wifi&' \
                   't={}&c_win=w_320_h_568&p_url={}&' \
                   'c_ostype=ios&jsoncallback=?&c_ctrl=w_search_trend0_f_content&methodName=getBiJiaInfo_wxsmall&c_devtype=phone&' \
                   'jgzspic=no&c_operator=中国移动&c_appver=3.6.0&bj=false&c_dp=2&c_osver=10.3.3'.format(
            int(time.time() * 1000), item_encoded)

        response = requests.get(url=url, data=postdata, headers=headers, verify=False)
        req = response.text
        # 解析返回的JSON数据
        js = json.loads(req)
        # 获取价格趋势数据
        jiagequshi = js['single']['jiagequshi']
        print(jiagequshi)
        print("helo the type is", type(jiagequshi))
        # 数据清洗
        datalist = jiagequshi.replace('[Date.UTC(', '').replace(')', '').replace(']', '').split(',')
        date_list = []  # 日期列表
        price_list = []  # 价格列表
        for i in range(0, len(datalist), 5):
            price = float(datalist[i + 3])
            date_list.append((int(datalist[i]), int(datalist[i + 1]) + 1, int(datalist[i + 2])))
            price_list.append(price)
        if price_list:
            latest_price = price_list[-1]  # 获取最新价格（最后一个价格）
            return latest_price
        else:
            return None
    except Exception as e:
        print(f"获取价格失败: {e}")
        return None


def send_price_drop_email(email, product_name, price, product_link):
    product_name = product_name.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    subject = f'您关注的商品"{product_name}"已降价'
    message = render_to_string('price_drop_alert.html', {
        'product_name': product_name,
        'price': price,
        'site_url': product_link,
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list, html_message=message)
        print(f"降价提醒邮件已发送至 {email}")
    except Exception as e:
        print(f"发送邮件失败: {e}")
