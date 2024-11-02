from django.shortcuts import render

# Create your views here.
# PriceDropAlert/views.py
from rest_framework import generics, permissions
from .models import PriceDropAlert
from .serializers import PriceDropAlertSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

class PriceDropAlertPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PriceDropAlertListCreateView(generics.ListCreateAPIView):
    serializer_class = PriceDropAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PriceDropAlertPagination

    def get_queryset(self):
        return PriceDropAlert.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PriceDropAlertRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PriceDropAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PriceDropAlert.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 只允许更新 target_price 和 active 字段
        data = request.data
        allowed_fields = ['target_price', 'active']
        update_data = {field: data[field] for field in allowed_fields if field in data}

        serializer = self.get_serializer(instance, data=update_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
