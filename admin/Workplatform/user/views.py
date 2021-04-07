# -*- coding: utf-8 -*-
import os

from taskmanage.utils import write_sys_log
from util.logging_checked import def_login_check, class_login_check
from util.response_code import code
from user.models import UserInfo, SearchEngine
from django.http import JsonResponse
from django.views.generic.base import View
from util.util import make_token, judge_data_complate, encode_md5, decode_passwd


@def_login_check
def create(request):
    if request.method == 'POST':
        body_data = request.body
        myuser = request.myuser
        if myuser.user_permission != 1:
            return JsonResponse(code[10410])
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        name = data.get('username')
        f_passwd_f = str(data.get('f_passwd'))
        s_passwd_s = str(data.get('s_passwd'))
        try:
            f_passwd = decode_passwd(f_passwd_f)
            s_passwd = decode_passwd(s_passwd_s)
        except Exception as e:
            return JsonResponse(code[10409])
        if f_passwd != s_passwd:
            return JsonResponse(code[10003])
        try:
            flag = UserInfo().create_user(data, s_passwd)
            if not flag:
                return JsonResponse(code[10002])
        except Exception as e:
            return JsonResponse(code[10401])
        # 签发token
        action_info = f'创建用户: [{name}]'
        write_sys_log(action_info, myuser)
        res_data = code[200]
        res_data['token'] = make_token(name).decode()
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


def login(request):
    if request.method == 'POST':
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        name = data.get('username')
        passwd_ = data.get('passwd')
        try:
            passwd = decode_passwd(passwd_)
        except Exception as e:
            return JsonResponse(code[10409])
        try:
            user = UserInfo.objects.get(name=name)
        except Exception as e:
            return JsonResponse(code[10004])
        if user.password != encode_md5(passwd):
            return JsonResponse(code[10003])
        res_data = code[200]
        res_data['token'] = make_token(name).decode()
        res_data['user_id'] = user.id
        res_data['roles'] = user.user_permission
        res_data['username'] = user.name
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


class ActionUserInfo(View):
    """
    用户信息更新
    """
    @class_login_check
    def post(self, request):
        myuser = request.myuser
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        try:
            flag, username = UserInfo().update_user_info(data)
            if not flag:
                return JsonResponse(code[10004])
            action_info = f'修改用户: [{username}]'
            write_sys_log(action_info, myuser)
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            res_data = code[10403]
            res_data['info'] = e
            return JsonResponse(code[10403])

    @class_login_check
    def get(self, request):
        try:
            myuser = request.myuser
            user_id = request.GET.get('user_id')
            if not user_id:
                return JsonResponse(code[10004])
            flag, username = UserInfo().delete_user_info(user_id)
            if not flag:
                return JsonResponse(code[10402])
            action_info = f'删除用户: [{username}]'
            write_sys_log(action_info, myuser)
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            return JsonResponse(code[10402])


def get_user_info(request):
    """
    修改用户 或 key基本信息
    :param request: 根据key_word 判断修改的为用户信息 还是key信息
    :return:
    """
    if request.method == "GET":
        page = request.GET.get('page')
        max_count = request.GET.get('max_count')
        search_word = request.GET.get('search_word')
        try:
            data_dic = UserInfo().query_user_info(page, max_count, search_word)
            res_data = code[200]
            res_data['data'] = data_dic['data']
            res_data['total'] = data_dic['total_page']
        except Exception as e:
            print(e)
            err_data = code[60003]
            err_data['info'] = str(e)
            return JsonResponse(err_data)
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


def get_all_user_info(request):
    if request.method == "GET":
        result = UserInfo().get_all_user()
        res_data = code[200]
        res_data['data'] = result['data']
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


class CreateDelKey(View):
    @class_login_check
    def post(self, request):
        """
        创建api_key
        """
        myuser = request.myuser
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        account_key = SearchEngine().create_key(data)
        action_info = f'创建信息收集账号: [{account_key}]'
        write_sys_log(action_info, myuser)
        return JsonResponse(code[200])

    @class_login_check
    def get(self, request):
        """
        删除api_key
        """
        myuser = request.myuser
        engine_id = request.GET.get('engine_id')
        if not engine_id:
            return JsonResponse(code[10004])
        flag, account = SearchEngine().delete_engine_info(engine_id)
        if not flag:
            return JsonResponse(code[10406])
        action_info = f'删除信息收集账号: [{account}]'
        write_sys_log(action_info, myuser)
        return JsonResponse(code[200])


class ModifyQueryKey(View):
    """
    修改 search engine
    """
    @class_login_check
    def post(self, request):
        myuser = request.myuser
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        flag, account = SearchEngine().modify_search_engine(data)
        if not flag:
            return JsonResponse(code[10406])
        action_info = f'修改信息收集账号: [{account}]'
        write_sys_log(action_info, myuser)
        return JsonResponse(code[200])

    def get(self, request):
        """
        查询 search engine
        """
        try:
            page = request.GET.get('page')
            max_count = request.GET.get('max_count')
            search_word = request.GET.get('search_word')
            result, total_page = SearchEngine().query_engin_info(page, max_count, search_word)
            res_data = code[200]
            res_data['data'] = result
            res_data['total'] = total_page
            return JsonResponse(res_data)
        except Exception as e:
            return JsonResponse(code[10408])
