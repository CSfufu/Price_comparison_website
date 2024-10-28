from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='商品名称')
    product_id = models.CharField(max_length=50, unique=True, verbose_name='商品ID')
    platform = models.CharField(max_length=50, verbose_name='平台名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    link = models.URLField(verbose_name='商品链接')
    image_url = models.URLField(verbose_name='图片链接', null=True, blank=True)
    store_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='店铺名称')
    store_link = models.URLField(verbose_name='店铺链接', null=True, blank=True)
    # 添加其他需要的字段

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 使用 settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='search_histories'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    search_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-search_time']

    def __str__(self):
        return f"{self.user.username} searched {self.product.name} at {self.search_time}"


class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    date = models.DateField(verbose_name='日期')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')

    class Meta:
        unique_together = ('product', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.product.name} - {self.date} - {self.price}"