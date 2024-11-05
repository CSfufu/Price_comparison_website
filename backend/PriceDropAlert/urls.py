# PriceDropAlert/urls.py
from django.urls import path
from .views import PriceDropAlertListCreateView, PriceDropAlertRetrieveUpdateDestroyView, PriceDropAlertCreateView

urlpatterns = [
    path('', PriceDropAlertListCreateView.as_view(), name='price_drop_alert_list_create'),
    path('create/', PriceDropAlertCreateView.as_view(), name='price_drop_alert_create'),
    path('<int:id>/', PriceDropAlertRetrieveUpdateDestroyView.as_view(), name='price_drop_alert_detail'),
]
