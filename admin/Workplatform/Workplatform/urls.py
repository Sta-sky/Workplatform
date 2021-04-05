# -*- coding: utf-8 -*-
"""Workplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from Workplatform import settings
from django.urls import path,include

urlpatterns = [
    path(r'api/admin/', admin.site.urls),
    path(r'api/user/v1/', include('user.urls')),
    path(r'api/task/v1/', include('taskmanage.urls')),
    path(r'api/back/v1/', include('back_log.urls')),
    path(r'api/log/v1/', include('back_log.urls')),
    path(r'api/file/v1/', include('taskmanage.urls')),
    path('api/', include('adminq.urls')),
    path('api/mind/', include("mind.urls"))
]

