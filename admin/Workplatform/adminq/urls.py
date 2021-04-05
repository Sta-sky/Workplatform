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
from django.urls import path
from . import views

urlpatterns = [
    path('system/Operation/list', views.OperationListView.as_view()),
    path('system/summary', views.SystemInfoView.as_view()),
    path('system/backups', views.BackupList.as_view()),
    path('system/backup_down', views.BackupDown.as_view()),
    path('task/info', views.TaskInfo.as_view()),
    path('task/host/list', views.HostList.as_view()),
    path('task/host', views.HostView.as_view()),
    path('task/host/ports', views.HostPortListView.as_view()),
    path('task/vulnerability', views.VulnerabilityView.as_view()),
    path('task/vulnerability/list', views.VulnerabilityListView.as_view()),
    path('task/certificate/list', views.CertificateListView.as_view()),
    path('task/certificate', views.CertificateView.as_view()),
    path('test', views.test.as_view()),
]
