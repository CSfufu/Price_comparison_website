from django.db import models

# Create your models here.
from django.db import models


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
