from celery import Celery
import os

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Workplatform.settings")
django.setup()

# 配置  celery的中间键
broken = "redis://127.0.0.1/2"
backend = "redis://127.0.0.1/3"
# 初始化celery
celery_app = Celery('Workplatform', broker=broken, backend=backend)
# 加载配置文件
celery_app.config_from_object('Workplatform.settings')
# 自动注册任务
celery_app.autodiscover_tasks(
    ["celery_tasks"]
)
