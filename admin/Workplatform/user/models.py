# -*- coding: utf-8 -*-
from django.db import models, transaction

from util.redis_connect import Redis
from util.util import encode_md5, get_total_page, get_page_info_list


class UserInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=100, verbose_name='用户密码')
    user_permission = models.IntegerField(verbose_name='用户权限', null=False)
    email = models.EmailField(verbose_name='邮箱', null=True)
    phone = models.BigIntegerField(verbose_name='手机号码')
    task_count = models.IntegerField(verbose_name='任务数量', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_info'
        verbose_name_plural = '用户信息表'

    @classmethod
    def update_user_info(cls, data):
        """
        更新用户信息
        :param data: 用户信息字典
        :return:
        """
        user_id = int(data.get('user_id'))
        name = data.get('username')
        permission = int(data.get('permission'))
        phone = data.get('phone')
        email = data.get('email')
        try:
            user = UserInfo.objects.get(id=user_id)
            if not user:
                return False
            with transaction.atomic():
                user.user_permission = permission
                user.name = name
                user.phone = phone
                user.email = email
                user.save()
            del_user_info_cache()
            return True, name
        except Exception as e:
            return False, None

    @classmethod
    def create_user(cls, data, passwd):
        """
        创建用户
        :param data: 用户信息字典
        :return:
        """
        name = data.get('username')
        phoen = data.get('phone')
        email = data.get('email')
        permission = data.get('permission')
        user = UserInfo.objects.filter(name=name)
        passwd = encode_md5(passwd)
        if user:
            return False
        try:
            with transaction.atomic():
                create_user = UserInfo.objects.create(
                    name=name,
                    password=passwd,
                    user_permission=permission,
                    phone=phoen,
                    email=email
                )
                create_user.save()
            UserInfo().del_user_info_cache()
            return True
        except Exception as e:
            return False

    @classmethod
    def query_user_info(cls, page, max_count, search_word):
        """
        查询用户基本信息
        """
        data_dic = {}
        redis_obj = Redis('user')
        redis_key = 'user_info'
        try:
            if search_word:
                redis_filed = 'user_dict_' + page + '_' + search_word + '_' + max_count
                print(redis_filed)
                data, flag = redis_obj.is_not_hit_hget_cache(redis_key, redis_filed)
                if flag:
                    print('用户搜索命中缓存')
                    return data
                user_info = UserInfo.objects.filter(name__icontains=search_word)
                total_page = get_total_page(user_info, max_page=max_count)
                page_info_list = get_page_info_list(user_info, max_count, page)
                data = UserInfo().user_obj_return_info(page_info_list)
            else:
                redis_filed = 'user_dict_' + page + '_' + max_count
                print(redis_filed)
                data, flag = redis_obj.is_not_hit_hget_cache(redis_key, redis_filed)
                if flag:
                    print('用户信息命中缓存')
                    return data
                user_info = UserInfo.objects.all()
                total_page = get_total_page(user_info, max_page=max_count)
                page_info_list = get_page_info_list(user_info, max_count, page)
                data = UserInfo().user_obj_return_info(page_info_list)
            data_dic['data'] = data
            data_dic['total_page'] = total_page
            print(redis_key, redis_filed)
            redis_obj.dic_type_write_cache(redis_key, redis_filed, data_dic)
            return data_dic
        except Exception as e:
            raise e

    @classmethod
    def user_obj_return_info(cls, page_info_list):
        data_list = []
        for info in page_info_list:
            data_dic = {
                'id': info.id,
                'name': info.name,
                'email': info.email,
                'phone': info.phone,
                'task_count': info.task_count,
                'user_permission': info.user_permission
            }
            data_list.append(data_dic)
        return data_list

    @classmethod
    def delete_user_info(cls, user_id):
        """删除用户"""
        try:
            user = UserInfo.objects.get(id=user_id)
            name = user.name
            user.delete()
            del_user_info_cache()
            return True, name
        except Exception as e:
            print(e)
            return False, None

    @classmethod
    def get_all_user(cls):
        try:
            data_dic = {}
            redis_obj = Redis('user')
            redis_key = 'all_user_info'
            redis_filed = 'all_user_dict'
            data, flag = redis_obj.is_not_hit_hget_cache(redis_key, redis_filed)
            if flag:
                print('所有用户命中缓存')
                return data
            user_list = []
            user = UserInfo.objects.all()
            for info in user:
                user_dic = {
                    'id': info.id,
                    'name': info.name
                }
                user_list.append(user_dic)
            data_dic['data'] = user_list
            redis_obj.dic_type_write_cache(redis_key, redis_filed, data_dic)
            return data_dic
        except Exception:
            raise

    @classmethod
    def del_user_info_cache(cls):
        redis_obj = Redis('user')
        ress = redis_obj.redis_delete('user_info')
        res = redis_obj.redis_delete('all_user_info')
        print(res)
        print(ress)
        print('删除用户成功')


class SearchEngine(models.Model):
    account = models.CharField(max_length=50, verbose_name='账户')
    key = models.CharField(max_length=1000, verbose_name='key')
    engine_type = models.CharField(max_length=20, verbose_name='引擎类型')
    proxy = models.CharField(max_length=100, verbose_name='代理', null=True)

    class Meta:
        db_table = 'search_engine'

    @classmethod
    def create_key(cls, data):
        account = data.get('account')
        engine_type = data.get('engine_type')
        key = data.get('key')
        proxy = data.get('proxy')
        try:
            user = SearchEngine.objects.create(
                account=account,
                engine_type=engine_type,
                key=key,
                proxy=proxy
            )
            user.save()
            return account
        except Exception as e:
            print(e)
            raise

    @classmethod
    def modify_search_engine(cls, data):
        """
        修改 search engine
        """
        engine_id = data.get('engine_id')
        account = data.get('account')
        proxy = data.get('proxy')
        engine_type = data.get('engine_type')
        key = data.get('key')
        try:
            engine = SearchEngine.objects.get(id=engine_id)
            with transaction.atomic():
                engine.key = key
                engine.engine_type = engine_type
                engine.account = account
                engine.proxy = proxy
                engine.save()
            return True, account
        except Exception as e:
            return False, None

    @classmethod
    def delete_engine_info(cls, engine_id):
        """删除key信息"""
        try:
            with transaction.atomic():
                accout = SearchEngine.objects.get(id=engine_id)
                account = accout.account
                accout.delete()
            return True, account
        except Exception:
            return False, None

    @classmethod
    def query_engin_info(cls, page, max_count, search_word):
        """查询 搜索engine"""
        try:
            if search_word:
                key_info = SearchEngine.objects.filter(account__icontains=search_word)
                total_page = get_total_page(key_info, max_page=max_count)
                page_info_list = get_page_info_list(key_info, max_count, page)
                data = SearchEngine().user_obj_return_key_info(page_info_list)
                return data, total_page

            else:
                key_info = SearchEngine.objects.all()
                total_page = get_total_page(key_info, max_page=max_count)
                page_info_list = get_page_info_list(key_info, max_count, page)
                data = SearchEngine().user_obj_return_key_info(page_info_list)
                return data, total_page
        except Exception as e:
            print(e)
            raise e

    @classmethod
    def user_obj_return_key_info(cls, page_info_list):
        data_list = []
        for info in page_info_list:
            data_dic = {
                'id': info.id,
                'account': info.account,
                'key': info.key,
                'engine_type': info.engine_type,
                'proxy': info.proxy
            }
            data_list.append(data_dic)
        return data_list
