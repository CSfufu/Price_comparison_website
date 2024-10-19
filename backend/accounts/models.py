from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 如果需要添加额外的字段，可以在这里定义
    pass
