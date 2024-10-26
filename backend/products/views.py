from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .utils.jd import jd_request_search
from .utils.taobao import tb_request_search
from django.http import JsonResponse
import concurrent.futures
from .serializers import ProductModelSerializer, ProductDictSerializer
import re


def clean_title(title):
    """
    移除 HTML 标签并返回纯文本标题。
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', title)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def jd_search_view(request):
    """
    处理京东商品搜索请求
    """
    data = request.data
    keyword = data.get('keyword')
    cookie = data.get('cookie')
    offset = data.get('offset', 0)
    limit = data.get('limit', 30)

    if not keyword or not cookie:
        return JsonResponse({'error': 'Missing required parameters: keyword and cookie.'}, status=400)

    try:
        search_results = jd_request_search(keyword, cookie, offset, limit)
        return JsonResponse(search_results, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tb_search_view(request):
    """
    处理京东商品搜索请求
    """
    data = request.data
    keyword = data.get('keyword')
    cookie = data.get('cookie')
    offset = data.get('offset', 0)
    limit = data.get('limit', 30)

    if not keyword or not cookie:
        return JsonResponse({'error': 'Missing required parameters: keyword and cookie.'}, status=400)

    try:
        search_results = tb_request_search(keyword, cookie, offset, limit)
        return JsonResponse(search_results, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_all_view(request):
    data = request.data
    keyword = data.get('keyword')
    cookie_jd = data.get('cookie_jd', '')
    cookie_tb = data.get('cookie_tb', '')
    offset = int(data.get('offset', 0))
    limit = int(data.get('limit', 30))

    if not keyword or (not cookie_jd and not cookie_tb):
        return JsonResponse(
            {'error': 'Missing required parameters: keyword and at least one cookie (cookie_jd or cookie_tb).'},
            status=400)

    try:
        # 使用 ThreadPoolExecutor 并行执行爬虫
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            if cookie_jd:
                futures.append(executor.submit(jd_request_search, keyword, cookie_jd, offset, limit // 2))
            if cookie_tb:
                futures.append(executor.submit(tb_request_search, keyword, cookie_tb, offset, limit // 2))

            results = [future.result() for future in futures]

        combined_results = {}
        if len(results) == 2:
            combined_results['jd'], combined_results['tb'] = results
        elif cookie_jd:
            combined_results['jd'] = results[0]
        elif cookie_tb:
            combined_results['tb'] = results[0]

        print("combined_results done correctly123")
        response_data = {}
        for platform in combined_results:
            data = combined_results[platform]
            products = data.get('results', [])[:20]
            total = data.get('total', 0)
            if platform == 'tb':
                # 淘宝数据需要字段映射和清理
                mapped_products = []
                for item in products:
                    #print(item)
                    #print(item.get('title'))
                    mapped_product = {
                        'name': ''.join(clean_title(item.get('title', ''))),
                        'product_id': item.get('item_id', ''),
                        'platform': '淘宝',
                        'price': float(item.get('price', '0').replace(',', '')) if item.get('price') else 0.0,
                        'link': f"https:{item.get('auctionURL', '')}" if item.get('auctionURL') else '',
                        'image_url': item.get('pic_path', ''),
                        'store_name': item.get('nick', ''),
                        'store_link': f"https:{item.get('shopInfo', {}).get('url', '')}" if item.get(
                            'shopInfo') else '',
                    }
                    # print(mapped_product['product_id'], type(mapped_product['product_id']))
                    # print("mapped_product done")
                    mapped_products.append(mapped_product)
                    # print(mapped_products)
                serializer = ProductDictSerializer(mapped_products, many=True)
                # 确保 total 是数字类型
                response_data[platform] = {
                    'results': serializer.data,
                    'total': total
                }
                print("taobao done")
            elif platform == 'jd':
                # 京东数据直接序列化
                mapped_products = []
                count = 0
                for item in products:
                    # print(item)
                    # print(item.get('info', {}).get('title', ''))
                    # print(count, total)
                    mapped_product = {
                        'name': ''.join(clean_title(item.get('info', {}).get('title', ''))),
                        'product_id': item.get('sku', ''),
                        'platform': '京东',
                        'price': float(item.get('price', '0').replace(',', '')) if item.get('price') else 0.0,
                        'link': item.get('info', {}).get('link', ''),
                        'image_url': item.get('imgSrc', ''),
                        'store_name': item.get('store', {}).get('title', ''),
                        'store_link': item.get('store', {}).get('link', ''),
                    }
                    # print(mapped_product['product_id'], type(mapped_product['product_id']))
                    mapped_products.append(mapped_product)
                    count += 1
                    # print(count)
                # print(mapped_products)
                serializer = ProductDictSerializer(mapped_products, many=True)
                # 确保 total 是数字类型
                response_data[platform] = {
                    'results': serializer.data,
                    'total': total
                }
                print("jingdong done")

        return Response(response_data, status=200)


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        serializer = ProductModelSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': '商品不存在'}, status=404)