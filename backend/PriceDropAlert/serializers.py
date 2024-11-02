# PriceDropAlert/serializers.py
from rest_framework import serializers
from .models import PriceDropAlert

class PriceDropAlertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_link = serializers.URLField(source='product.link', read_only=True)
    current_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = PriceDropAlert
        fields = ['id', 'product', 'target_price', 'email', 'active']
        read_only_fields = ['id', 'active']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data.get('product')
        target_price = validated_data.get('target_price')
        email = user.email  # 从关联用户获取邮箱

        alert = PriceDropAlert.objects.create(
            user=user,
            product=product,
            target_price=target_price,
            email=email,
            active=False  # 默认不激活
        )
        return alert
