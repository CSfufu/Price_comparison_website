# serializers.py
from rest_framework import serializers
from .models import PriceDropAlert
from products.models import Product


class PriceDropAlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_link = serializers.URLField(source='product.link', read_only=True)
    image_url = serializers.URLField(source='product.image_url', read_only=True)
    current_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    email = serializers.EmailField(required=True)  # 确保邮箱是必填的
    product_id = serializers.CharField(write_only=True)  # 接受 product_id 字段（前端传递的字段）

    class Meta:
        model = PriceDropAlert
        fields = ['id', 'product_id', 'target_price', 'email', 'active', 'current_price', 'product_name',
                  'product_link', 'image_url']
        read_only_fields = ['id', 'product_name', 'product_link', 'current_price', 'image_url']

    def create(self, validated_data):
        # 获取产品ID
        product_id = validated_data.get('product_id')

        # 使用传入的 product_id 查找对应的 Product 实体
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with id {product_id} not found.")

        # 创建 PriceDropAlert 实例
        alert = PriceDropAlert.objects.create(
            user=self.context['request'].user,
            product=product,
            target_price=validated_data.get('target_price'),
            email=validated_data.get('email'),
            active=validated_data.get('active', False))
        # 默认 inactive
        return alert
