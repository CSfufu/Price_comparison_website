import pymysql
pymysql.install_as_MySQLdb()

# backend/__init__.py

# backend/__init__.py
from .celery import app as celery

__all__ = ('celery',)
