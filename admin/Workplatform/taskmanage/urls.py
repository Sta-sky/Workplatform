# -*- coding: utf-8 -*-
# from django.conf.urls import url
from django.urls import path

from taskmanage import views
from taskmanage import search

urlpatterns = [
    path(r'add_del_task', views.CreateDeleteTask.as_view()),             # 任务、创建、删除
    path(r'modify_query_task', views.QueryModifyTask.as_view()),         # 任务、查询、修改、搜索
    path(r'task_detail', views.task_detail),                             # 任务详情查询
    path(r'add_del_subdir', views.AddSubDir.as_view()),                  # 文件目录创建以及删除
    path(r'modify_query_subdir', views.ModifyQueryDir.as_view()),        # 文件目录修改以及查询
    path(r'add_del_note', views.AddDelNote.as_view()),                   # 笔记添加，删除
    path(r'modify_query_note', views.ModifyqueryNot.as_view()),          # 笔记修改，查询
    path(r'edit_note', views.edit_note),                                 # 笔记编辑
    path(r'upload_notes', views.uploade_notes),                          # 笔记批量上传
    path(r'upload_img', views.UploadeImg.as_view()),                     # 笔记批量上传
    path(r'add_file_dir', views.AddDelDir.as_view()),                    # 添加 删除文件目录
    path(r'modify_query_dir', views.ModifyQueryFileDir.as_view()),       # 添加 删除文件目录
    path(r'add_del_file', views.AddDelFile.as_view()),                   # 添加、删除文件
    path(r'download_file', views.download_files),                        # 下载、文件
    path(r'download_note', views.download_note),                         # 笔记下载
    path(r'note_file_search', views.note_file_search),                     # 笔记搜索
    path(r'knowledge_lib', views.knowledge_primary_page),                # 知识点，笔记搜索
    path(r'knowledge_detail', views.know_note_details),                  # 知识点，笔记、备份详情查询
    path(r'add_del_label', views.AddDelLabel.as_view()),                 # 新增、删除 标签
    path(r'modify_query_label', views.ModifyQueryLabel.as_view()),       # 修改、查询、标签
    path(r'modify_query_label', views.ModifyQueryLabel.as_view()),       # 修改、查询、标签
    path(r'allsearch', search.all_search),                                # 全局搜索
]