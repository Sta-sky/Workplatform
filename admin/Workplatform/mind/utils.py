# -*- coding: utf-8 -*-
import datetime
import ipaddress
import os
import random
import socket

import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_redis import get_redis_connection
from tldextract import tldextract

from Workplatform.settings import BASE_DIR
from adminq.models import Host, TaskPort, ServerPort, TaskProgress
from mind.models import MindNode
from mind.serializers import MindTreeSerializer
import geoip2.database
from elasticsearch import Elasticsearch

es = Elasticsearch()


def get_dir(page, page_size, node_id):
    body = {
        "query": {
            "match": {
                "node_id": str(node_id)
            }
        },
        "from": (page - 1) * page_size,
        "size": page_size
    }

    result = es.search(index="dirsearch", body=body)
    res_data = result['hits']['hits']
    res = []
    for item in res_data:
        item['_source']['id'] = item['_id']
        res.append(item['_source']["content"])
    return res


class NoteLock(object):
    def __init__(self, node_id):
        self.key = node_id
        self.redis_node = get_redis_connection("note")

    def get_node_lock_redis(self):
        is_lock = self.redis_node.get(self.key)
        return is_lock

    def set_lock(self, username):
        is_lock = self.redis_node.get(self.key)
        if is_lock:
            # todo 这里会加锁
            self.redis_node.delete(self.key)
        print(username)
        self.redis_node.set(self.key, username, 300)

    def delete_lock(self, username):
        is_lock = self.redis_node.get(self.key)
        if is_lock:
            is_lock = is_lock.decode()
            if is_lock != username:
                return False
            else:
                self.redis_node.delete(self.key)
                return True
        else:
            return False


def task_progress(weight, task_id):
    if weight in [2, 3, 4]:
        TaskProgress.objects.filter(weight__lte=weight, task_id=task_id, update_time__isnull=True).update(
            update_time=datetime.datetime.now())
    else:
        task_list = TaskProgress.objects.filter(weight__lte=weight, task_id=task_id, update_time__isnull=True)
        count = task_list.count()
        if weight - count <= 3:
            task_list.update(update_time=datetime.datetime.now())


def get_region(ip):
    try:
        path = BASE_DIR + "/util/GeoLite2-City/GeoLite2-City.mmdb"
        reader = geoip2.database.Reader(path)
        response = reader.city(ip)
        country = response.country.names.get('zh-CN')
        city = response.city.names.get('zh-CN')
        if country and city:
            region = country + " " + city
        elif country and not city:
            region = country
        elif city and not country:
            region = city
        else:
            region = '未知'
    except Exception as e:
        print(e)
        region = '未知'
    return region


def get_ip_list(domain):  # 获取域名解析出的IP列表
    ip_list = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
    except Exception as e:
        # print(str(e))
        pass
    return ip_list


def check_node_name(name, node, task_id, request):
    node_type = 4
    # Host.objects.filter(node=node, name=node.name).update(name=name)
    try:
        ipaddress.ip_network(name)
        ascription = get_region(name)
        print(node, node.name)
        Host.objects.filter(node=node, ip=node.name).update(ip=name)
        node.ascription = ascription
        node.save()
        node_type = 1
    except:
        pass
    try:
        host_list = ipaddress.ip_network(name, strict=False).host()
        for i in host_list:
            Host.objects.create(node=node, ip=i, task_id=task_id, user=request.myuser)
        node_type = 2
    except:
        pass
    full_domain = tldextract.extract(name).fqdn
    if full_domain:
        ip_list = get_ip_list(name)
        for i in ip_list:
            ip_list = Host.objects.filter(node=node, ip=i)
            if not ip_list:
                Host.objects.create(name=name, node=node, ip=i, task_id=task_id, user=request.myuser)
            else:
                ip_list.update(name=name)
        node_type = 3
    is_ip = name.split(":")[0]
    try:
        ipaddress.ip_network(is_ip)
        port = int(name.split(":")[1])
        ser_name = ServerPort.objects.filter(port=port).first()
        if ser_name:
            port_name = ser_name.server
        else:
            port_name = '未知'
        ip_list = Host.objects.filter(node=node, ip=is_ip)
        if not ip_list:
            host = Host.objects.create(node=node, ip=is_ip, task_id=task_id, user=request.myuser)
        else:
            host = ip_list.first()
        TaskPort.objects.create(host=host, port=port, name=port_name, task_id=task_id, node=node)
        node_type = 1
    except:
        pass
    return node_type


def update_mind(mind_id, info):
    mind_note = MindNode.objects.filter(mind_id=mind_id)
    content = MindTreeSerializer(mind_note, many=True)
    channel_layer = get_channel_layer()
    data = {
        "data": content.data,
        "info": info
    }
    async_to_sync(channel_layer.group_send)(f"mind_{mind_id}",
                                            {"type": "chat1.message", "message": data})


def check_node_lock(node_id, is_delete=True):
    is_lock = NoteLock(node_id=node_id).get_node_lock_redis()
    if is_lock:
        is_delete = False
        return is_delete
    else:
        node = MindNode.objects.filter(child_id=node_id)
        if node:
            for i in node:
                print(i.id)
                r_data = check_node_lock(i.id)
                is_delete = r_data
            return is_delete
        else:
            return is_delete


def create_note(node_id, data, n=1, child=0):
    node = MindNode.objects.filter(child_id=node_id)
    for i in node:
        if i.child != child:
            n += 1
            child = i.child
        if i.note:
            data1 = data + "#" * n + i.name + "\n\r" + "\t" + i.note + "\n\n\n"
        else:
            data1 = data
        data, n = create_note(i.id, data1, n, child)

    return data, n


def request_zoomeye_api(site, flag, page, config={}):
    # if config.get('zoomeye'):
    #     key = config.get('zoomeye')
    # else:
    #     key = random.choice(zoomeye_api_keys)
    headers = {
        'API-KEY': "D85a12af-136B-7017E-5CD9-dF79C0ffb1a"
    }
    if flag == 1:  # ip
        url = f'https://api.zoomeye.org/host/search?query=ip:{site}&page={page}'
        try:
            res = requests.get(url, headers=headers, timeout=30)
        except Exception as e:
            print('zoomeye请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip'], 'timestamp': item['timestamp'],
                    'portinfo': {'port': item['portinfo']['port'], 'service': item['portinfo']['service']},
                    'country': item['geoinfo']['country']['names']['zh-CN'], 'info': item['portinfo']['banner']} for
                   item in data['matches']]
        return {
            'total': total,
            'data': matches
        }
    elif flag == 2:  # 域名
        url = f'https://api.zoomeye.org/host/search?query=site:{site}&page={page}'
        try:
            res = requests.get(url, headers=headers, timeout=30)
        except Exception as e:
            print('zoomeye请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip'], 'timestamp': item['timestamp'],
                    'portinfo': {'port': item['portinfo']['port'], 'service': item['portinfo']['service']},
                    'country': item['geoinfo']['country']['names']['zh-CN'], 'info': item['portinfo']['banner']} for
                   item in data['matches']]
        return {
            'total': total,
            'data': matches
        }
    elif flag == 3:  # 网段
        url = f'https://api.zoomeye.org/host/search?query=cidr:{site}&page={page}'
        try:
            res = requests.get(url, headers=headers, timeout=30)
        except:
            print('zoomeye请求超时/出错')
            return {}
        try:
            data = res.json()
        except:
            print('返回出错')
            return {}
        total = data['total']
        matches = [{'ip': item['ip'], 'timestamp': item['timestamp'],
                    'portinfo': {'port': item['portinfo']['port'], 'service': item['portinfo']['service']},
                    'country': item['geoinfo']['country']['names']['zh-CN'], 'info': item['portinfo']['banner']} for
                   item in data['matches']]
        return {
            'total': total,
            'data': matches
        }

    else:
        return {}
