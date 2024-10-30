from django.urls import path, include
from .views import jd_search_view, tb_search_view, search_all_view, product_detail_view, SearchHistoryViewSet, \
    get_price_history_by_url, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'search_history', SearchHistoryViewSet, basename='search_history')
router.register(r'products_history', ProductViewSet, basename='products_history')


urlpatterns = [
    # ... 其他 URL
    path('jd_search/', jd_search_view, name='jd_search'),
    path('tb_search/', tb_search_view, name='tb_search'),
    path('search/', search_all_view, name='search_all'),
    path('price_history/', get_price_history_by_url, name='price_history'),
    path('', include(router.urls)),
    path('<str:product_id>/', product_detail_view, name='product_detail'),


]
