from rest_framework import serializers
from .models import Product


class ProductDictSerializer(serializers.Serializer):
    name = serializers.CharField()
    product_id = serializers.CharField()
    platform = serializers.CharField()
    price = serializers.SerializerMethodField()
    link = serializers.URLField()
    image_url = serializers.URLField()
    store_name = serializers.CharField()
    store_link = serializers.URLField()

    def get_price(self, obj):
        return float(obj.get('price', 0.0))

class ProductModelSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name',
            'product_id',
            'platform',
            'price',
            'link',
            'image_url',
            'store_name',
            'store_link',
        ]

    def get_price(self, obj):
        return float(obj.price) if obj.price else 0.0

