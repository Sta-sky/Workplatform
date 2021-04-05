import os
import uuid
import ipaddress
import tldextract
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from mind.models import OpenDir, MindNode
from user.models import SearchEngine
from celery_tasks.tasks import dirsearch_task
from webscanApp.utils import request_shodan_io_api, request_zoomeye_api, whois_func

# Create your views here.


# 解析用户输入站点
def parse_site(site, flag):
    if flag == 1:  # ip
        try:
            res = ipaddress.IPv4Address(site).compressed
            return True, res
        except:
            return False, None
    elif flag == 2:  # 域名
        full_domain = tldextract.extract(site).fqdn
        reg_domain = tldextract.extract(site).registered_domain
        if (not full_domain) or (not reg_domain):
            return False, None
        else:
            return True, site
    elif flag == 3:  # 网段
        try:
            res = ipaddress.IPv4Network(site).compressed
            return True, res
        except:
            return False, None
    else:
        return False, None


# 读取配置，如代理ip，token或者api_key
def get_config():
    res = {}
    configures = SearchEngine.objects.all()
    for config in configures:
        if config.engine_type == 'shodan':
            res['shodan'] = config.key
        if config.engine_type == 'zoomeye':
            res['zoomeye'] = config.key
        if config.engine_type == 'proxy':
            res['proxy'] = config.proxy
    return res


# dirsearch扫描视图函数
class SiteDirSearchView(APIView):

    def post(self, request):
        res = {
            'success': True,
            'info': '',
            'data': ''
        }
        data = request.data
        node_id = data.get('node_id')  # 节点id
        if not node_id:
            return Response(data=res)
        node = MindNode.objects.filter(id=node_id).first()
        if not node:
            res['success'] = False
            res['info'] = '未找到节点'
            return Response(data=res)
        site = node.name
        report_name = uuid.uuid4().hex + '.json'
        config = get_config()
        dirsearch_task.apply_async(args=[site, report_name, config])
        res['data'] = report_name
        return Response(data=res)


# 获取站点dirsearch扫描结果
class DirSearchReportView(APIView):

    def get(self, request):
        res = {
            'success': True,
            'info': '',
            'data': ''
        }
        data = request.data
        node_id = data.get('node_id')
        report_name = data.get('report_name')
        dir_obj = OpenDir.objects.filter(note__id=node_id).get()
        if not dir_obj:
            search_dir = settings.BASE_DIR + '/webscanApp/dirsearch'
            report_dir = search_dir + '/reports'
            report_path = os.path.join(report_dir, report_name)
            if report_name and os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_data = f.read()
                    dir_obj = OpenDir()
                    dir_obj.note = MindNode.objects.get(id=node_id)
                    dir_obj.dir = report_data
                    dir_obj.save()
                    print(f'节点:{node_id} 保存目录扫描结果完毕')
                res['data'] = report_data
                return Response(data=res)
            res['success'] = False
            res['info'] = '信息不存在,请稍后再试'
            return Response(data=res)
        res['data'] = dir_obj.dir

        return Response(data=res)


# 站点基本信息扫描（shodan）
class ShodanInfoScanView(APIView):

    def post(self, request):
        res = {
            'success': True,
            'info': '',
            'data': None
        }
        data = request.data
        site = data.get('site', '')
        if not site:
            return Response(data=res)
        flag = data.get('flag')
        page = data.get('page', 1)
        if flag not in [1, 2, 3]:
            return Response(data=res)
        res_info, site_info = parse_site(site, flag)
        if not res_info:
            res['success'] = False
            res['info'] = '输入有误'
            return Response(data=res)
        # 读取配置
        config = get_config()

        res_data = request_shodan_io_api(site_info, flag, page, config)
        res['data'] = res_data

        return Response(data=res)


# zoomeye站点扫描
class ZoomEyeInfoScanView(APIView):

    def post(self, request):
        res = {
            'success': True,
            'info': '',
            'data': None
        }
        data = request.data
        site = data.get('site', '')
        if not site:
            return Response(data=res)
        flag = data.get('flag')
        page = data.get('page', 1)
        if flag not in [1, 2, 3]:
            return Response(data=res)
        res_info, site_info = parse_site(site, flag)
        if not res_info:
            res['success'] = False
            res['info'] = '输入有误'
            return Response(data=res)
        # 读取配置
        config = get_config()

        res_data = request_zoomeye_api(site_info, flag, page, config)
        res['data'] = res_data

        return Response(data=res)


# whois信息获取
class WhoisInfoScanView(APIView):

    def post(self, request):
        res = {
            'success': True,
            'info': '',
            'data': {}
        }
        data = request.data
        site = data.get('site', '')
        if not site:
            return Response(data=res)
        flag = data.get('flag')
        if flag != 2:
            return Response(data=res)
        res_info, site_info = parse_site(site, flag)
        if not res_info:
            return Response(data=res)
        res_data = whois_func(site_info)
        res['data'] = res_data

        return Response(data=res)
