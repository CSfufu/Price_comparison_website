from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Product
from .utils.jd import jd_request_search
from .utils.taobao import tb_request_search
from django.http import JsonResponse
import concurrent.futures
from .serializers import ProductSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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

        return JsonResponse(combined_results, status=200)
    except Exception as e:
        return JsonResponse({'error': 'Search failed. Please check your cookies and try again.'}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': '商品不存在'}, status=404)