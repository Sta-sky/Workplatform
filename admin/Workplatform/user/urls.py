# -*- coding: utf-8 -*-
from django.urls import path

from user import views

urlpatterns = [
    path(r'create', views.create),                                  # 用户注册
    path(r'login', views.login),                                    # 用户登录
    path(r'modify_del_user', views.ActionUserInfo.as_view()),       # 用户主页信息修改
    path(r'userinfo', views.get_user_info),                         # 用户页面信息 获取
    path(r'all_user', views.get_all_user_info),                     # 查询全部用户
    path(r'key_create_del', views.CreateDelKey.as_view()),          # 用户页面信息 修改
    path(r'key_modify_query', views.ModifyQueryKey.as_view()),      # 用户页面信息 修改

]