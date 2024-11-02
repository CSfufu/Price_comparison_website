# backend/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置默认的 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 创建 Celery 应用实例
app = Celery('backend')

# 从 Django 的 settings.py 中加载配置，所有以 CELERY 开头的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有已注册的 Django 应用中的 tasks.py 模块中的任务
app.autodiscover_tasks()

# 如果需要，可以添加一些测试任务或调试信息
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
