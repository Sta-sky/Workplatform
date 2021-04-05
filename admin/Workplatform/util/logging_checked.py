# -*- coding: utf-8 -*-
import jwt
from user.models import UserInfo
from util.response_code import code
from django.http import JsonResponse
from Workplatform.settings import JWT_TOKEN_KEY


def class_login_check(func):
    def wrapper(self, request, *args, **kwargs):
        # 获取用户的token
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                return JsonResponse(code[60002])
            res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
            username = res['username']
            user = UserInfo.objects.get(name=username)
        except Exception as e:
            return JsonResponse(code[10407])
        request.myuser = user
        return func(self, request, *args, **kwargs)
    return wrapper


def def_login_check(func):
    def wrapper(request, *args, **kwargs):
        # 获取用户的token
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                return JsonResponse(code[60002])
            res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
            username = res['username']
            user = UserInfo.objects.get(name=username)
        except Exception as e:
            return JsonResponse(code[10407])
        request.myuser = user
        return func(request, *args, **kwargs)
    return wrapper


def token_return_user(token):
    try:
        res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
        username = res['username']
        user = UserInfo.objects.get(name=username)
        return user
    except Exception as e:
        print(e)
        return False