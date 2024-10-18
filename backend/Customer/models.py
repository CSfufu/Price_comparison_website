from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Customer(AbstractUser):
    name = models.EmailField(unique=True)
