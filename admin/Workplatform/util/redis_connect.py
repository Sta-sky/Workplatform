# -*- coding: utf-8 -*-
import json
import time

from django_redis import get_redis_connection
from django_redis import cache


class Redis(object):
    def __init__(self, cache_type):
        self.expria = (60 * 60 * 24)
        self.redis_lib = cache_type
        self.redis_obj = get_redis_connection(cache_type)

    def dic_type_write_cache(
            self, redis_key=None, redis_filed=None, data=None, expira=3600):
        """
        data:
            type: dict
        """
        value = json.dumps(data)
        try:
            result = self.redis_obj.hset(redis_key, redis_filed, value)
            self.redis_obj.expire(redis_key, expira)
            return result, True
        except Exception as e:
            return e, False

    def is_not_hit_hget_cache(self, redis_key=None, redis_filed=None):
        try:
            result = self.redis_obj.hget(redis_key, redis_filed)
            if not result:
                return {}, False
            return json.loads(result), True
        except Exception as e:
            raise Exception(f'redis查询数据错误，错误原因为{e}')

    def redis_hexists(self, redis_key=None, redis_filed=None):
        """
            return : True or False
        """
        try:
            result = self.redis_obj.hexists(redis_key, redis_filed)
            return result
        except Exception:
            raise

    def redis_hdel(self, redis_key=None, redis_filed=None):
        """
        hash类型删除
        """
        try:
            result = self.redis_obj.delete(redis_key, redis_filed)
            if not result:
                return False
            return True
        except Exception as e:
            raise

    def redis_delete(self, redis_key=None):
        """
        删除 key
        """
        try:
            result = self.redis_obj.delete(redis_key)
            if not result:
                return False
            return True
        except Exception as e:
            raise

    def acquire_lock(self, note_id, time_out=1800):
        """
        获取一个分布式锁
            key 不存在： -2
            key 存在但没有设置剩余时间时：-1
        """
        try:
            lock = "note:lock:" + str(note_id)
            res = self.redis_obj.setnx(lock, note_id)
            if res:
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.redis_obj.expire(lock, time_out)
                return True, None
            if not res:
                ttls = self.redis_obj.ttl(lock)
                return False, ttls
        except Exception as e:
            raise

    def delete_lock(self, note_id):
        """删除一个分布式锁"""
        try:
            lock = "note:lock:" + str(note_id)
            self.redis_obj.delete(lock)
        except Exception:
            raise

