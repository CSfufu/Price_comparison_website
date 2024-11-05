from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PriceDropAlert
from .serializers import PriceDropAlertSerializer
from rest_framework.pagination import PageNumberPagination


class PriceDropAlertPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class PriceDropAlertListCreateView(generics.ListCreateAPIView):
    serializer_class = PriceDropAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PriceDropAlertPagination

    def get_queryset(self):
        return PriceDropAlert.objects.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': '降价提醒创建成功',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PriceDropAlertRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PriceDropAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PriceDropAlert.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 只允许更新特定字段
        allowed_fields = ['target_price', 'active']
        update_data = {
            field: request.data[field]
            for field in allowed_fields
            if field in request.data
        }

        serializer = self.get_serializer(
            instance,
            data=update_data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': '更新成功',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '删除成功'
        }, status=status.HTTP_200_OK)


class PriceDropAlertCreateView(APIView):
    """
        创建价格提醒
        """

    def post(self, request, *args, **kwargs):
        # 将前端数据传递给序列化器
        serializer = PriceDropAlertSerializer(data=request.data, context={'request': request})

        # 验证数据
        if serializer.is_valid():
            # 创建价格提醒
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 如果数据无效，返回错误信息
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)