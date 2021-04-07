from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('shodan', views.ShodanInfoScanView.as_view()),
    path('zoomeye', views.ZoomEyeInfoScanView.as_view()),
    path('whois', views.WhoisInfoScanView.as_view()),
    path('dirsearch', views.SiteDirSearchView.as_view()),
    path('dirsearch/report', views.DirSearchReportView.as_view()),
]