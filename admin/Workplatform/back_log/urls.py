# -*- coding: utf-8 -*-
from django.urls import path
from back_log import views

urlpatterns = [
    path(r'query_back_data', views.query_all_backup_data),  # 备份数据的查询
    path(r'back_data', views.return_backup_data),  # 备份数据的查询
    path(r'file_log', views.query_file_note_log),  # 文件目录日志的查询

]
