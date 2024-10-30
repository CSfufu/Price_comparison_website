from rest_framework import serializers
from .models import Product, SearchHistory


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


class SearchHistorySerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True)
    class Meta:
        model = SearchHistory
        fields = "__all__"


class PriceHistorySerializer(serializers.Serializer):
    date = serializers.DateField()
    price = serializers.FloatField()


class ProductPriceHistoryResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    link = serializers.URLField()
    image_url = serializers.URLField()
    price_history = PriceHistorySerializer(many=True)


