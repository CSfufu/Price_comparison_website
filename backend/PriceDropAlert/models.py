# PriceDropAlert/models.py
from django.db import models
from django.conf import settings  # 用于获取自定义用户模型
from products.models import Product  # 假设 Product 模型在 products 应用中


class PriceDropAlert(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='price_drop_alerts'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='商品',
        related_name='price_drop_alerts'
    )
    target_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='目标价格'
    )
    email = models.EmailField(
        verbose_name='通知邮箱',
        blank=True,
        null=True
    )
    active = models.BooleanField(
        default=False,
        verbose_name='是否激活'
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - 目标价：￥{self.target_price}"
