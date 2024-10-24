from django.urls import path
from .views import jd_search_view, tb_search_view, search_all_view, product_detail_view

urlpatterns = [
    # ... 其他 URL
    path('jd_search/', jd_search_view, name='jd_search'),
    path('tb_search/', tb_search_view, name='tb_search'),
    path('search/', search_all_view, name='search_all'),
    path('<int:pk>/', product_detail_view, name='product_detail'),
]
