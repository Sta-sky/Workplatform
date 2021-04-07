# -*- coding: utf-8 -*-
# from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('mind_map', views.MindView.as_view()),
    path('create_mind', views.MindCreate.as_view()),
    path("mind_disconnect", views.MindDisconnect.as_view()),
    path("mind_node", views.MindNodeView.as_view()),
    path("lock_node", views.LockNode.as_view()),
    path("node", views.NodeDetail.as_view()),
    path("host_list_node", views.HostListView.as_view()),
    path("node_port_list", views.PortListView.as_view()),
    path("PortScan", views.PortScan.as_view()),
    path("create_note", views.CreateNote.as_view()),
    path("node_file", views.NoteFileView.as_view()),
    path("e_mind_log", views.EMindLog.as_view()),
    path("mind_log",views.MindLogView.as_view()),
    path("node_note",views.NoteView.as_view())

]
