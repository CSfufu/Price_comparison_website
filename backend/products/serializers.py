from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'product_id', 'platform', 'price', 'link', 'image_url', 'store_name', 'store_link']



    def get_price(self, obj):
        return float(obj.get('price', 0.0))
