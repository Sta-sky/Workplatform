# -*- coding: utf-8 -*-
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/mind/(?P<mind_id>\w+)/$', consumers.MindConsumer.as_asgi()),
    re_path(r"ws/online/(?P<mind_id>\w+)/$",consumers.OnlineConsumer.as_asgi())
]

