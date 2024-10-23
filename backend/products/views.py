from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .utils.jd import jd_request_search
from .utils.taobao import tb_request_search
from django.http import JsonResponse
import concurrent.futures



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
    cookie_jd = data.get('cookie_jd')
    cookie_tb = data.get('cookie_tb')
    offset = data.get('offset', 0)
    limit = data.get('limit', 30)

    if not keyword or not cookie_jd or not cookie_tb:
        return JsonResponse({'error': 'Missing required parameters: keyword, cookie_jd, and cookie_tb.'}, status=400)

    try:
        # 使用 ThreadPoolExecutor 并行执行爬虫
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_jd = executor.submit(jd_request_search, keyword, cookie_jd, offset, limit // 2)
            future_tb = executor.submit(tb_request_search, keyword, cookie_tb, offset, limit // 2)

            jd_results = future_jd.result()
            tb_results = future_tb.result()

        combined_results = {
            'jd': jd_results,
            'tb': tb_results,
        }

        return JsonResponse(combined_results, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
