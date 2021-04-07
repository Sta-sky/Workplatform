import json
import os
import re

import jwt
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.db.transaction import atomic
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from django.utils.timezone import now
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

# from mind.tasks import CourseTask
from adminq import tasks
from adminq.tasks import backup
# from rest_framework_jwt.authentication import jwt_decode_handler
from .models import OperatingLog, BackupRecord, Host, TaskPort, TaskVulnerability, TaskCertificate, TaskProgress, \
    ServerPort
from .serializers import SystemLogSerializer, HostListSerializer
from .utils import get_os_info, check_ip
from taskmanage.models import Task, NoteDir, FileDir, NoteLog, FileLog
from mind.utils import task_progress
from mind.models import MindLog

from util.logging_checked import class_login_check

from user.models import UserInfo

from Workplatform.settings import JWT_TOKEN_KEY

from mind.models import MindNode

progress_dict = {
    1: "隐蔽攻击源",
    2: "收集攻击目标信息",
    3: "挖掘漏洞信息",
    4: "获取目标访问权限",
    5: "隐蔽攻击行为",
    6: "实时攻击",
    7: "开辟后门",
    8: "清除攻击痕迹，销毁攻击源"

}


class test(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        for task in tasks:
            for k, v in progress_dict.items():
                TaskProgress.objects.create(name=v, weight=k, task=task)
        return Response(1)


class SystemInfoView(APIView):

    def get(self, *args, **kwargs):
        resp = {
            'success': True,
            'info': '',
            'data': {}
        }
        data = get_os_info()
        resp['data'] = data

        return Response(resp)


class OperationListView(APIView):

    @class_login_check
    def post(self, request):
        res = {
            'success': True,
            'info': '',
            'data': [],
            'total': 0
        }
        user = request.myuser
        data = request.data
        page = data.get('page', 1)
        page_size = data.get('page_size', 10)
        search = data.get('search')
        if user.user_permission == 1:
            objs = OperatingLog.objects.all().order_by('-create_time')
        else:
            objs = OperatingLog.objects.filter(operator_id=user.id).order_by('-create_time')
        if search:
            objs = objs.filter(content__icontains=search)
        res['total'] = objs.count()
        paginator = Paginator(objs, page_size)
        try:
            res_objs = paginator.page(page)
        except EmptyPage as e:
            print(e)
            res['info'] = 'no more info'
            return Response(data=res)
        ser_data = SystemLogSerializer(res_objs, many=True)
        res['data'] = ser_data.data
        return Response(data=res)

    def delete(self, request):
        res = {
            'success': True,
            'info': ''
        }
        data = request.data
        id = data.get('id')
        obj = OperatingLog.objects.filter(id=id)
        if not obj:
            res['success'] = False
            res['info'] = '未找到指定系统日志'
            return Response(data=res)
        obj.delete()

        return Response(data=res)


class BackupList(APIView):
    @class_login_check
    def post(self, request):
        # 数据库备份
        """
        mysqldump -uroot -p123 db1 > db1.sql
        :param request:
        :return:
        """
        # 1. 根据数据创建文件夹
        user = request.myuser
        back = BackupRecord.objects.create(progress=2, status=0)
        backup.delay(back.id)
        OperatingLog.objects.create(content=f"新增{back.create_time.strftime('%Y-%m-%d %H:%M:%S')}的数据备份",
                                    operator_id=user.id)
        # CourseTask.apply_async(args=(12,), queue='work_queue')
        return Response({"success": True, "info": ""})

    def get(self, request):
        page_size = request.query_params.get("page_size")
        back = BackupRecord.objects.filter().order_by("-create_time")
        page = PageNumberPagination()
        page.page_size = int(page_size)
        tasks = page.paginate_queryset(queryset=back, request=request, view=self)

        data_list = []

        for back_data in tasks:
            data = {
                "create_time": back_data.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": back_data.status,
                "id": back_data.id,
                "progress": back_data.progress
            }
            data_list.append(data)

        return Response({"success": True, "data": data_list, "total": back.count()})

    @class_login_check
    def delete(self, request):
        user = request.myuser
        back_id = request.data.get("id")
        back = BackupRecord.objects.filter(id=back_id).first()
        if back:
            file_path = back.backup_filepath
            try:
                os.remove(file_path)

            except Exception as e:
                pass
            back.delete()
            OperatingLog.objects.create(content=f"删除{back.create_time.strftime('%Y-%m-%d %H:%M:%S')}的数据备份",
                                        operator_id=user.id)
            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": "参数错误！"})


class BackupDown(APIView):

    def post(self, request):
        back_id = request.data.get("id")
        back = BackupRecord.objects.filter(id=back_id).first()
        if back:
            url = "/system/backup_down?id=" + str(back.id)
            return Response({"success": True, "url": url})
        else:
            return Response({"success": False, "info": "参数错误！"})

    def get(self, request):
        back_id = int(request.query_params.get("id"))
        token = request.query_params.get("token")
        try:
            res = jwt.decode(token, JWT_TOKEN_KEY, algorithms='HS256')
            username = res['username']
            user = UserInfo.objects.filter(name=username).first()
            user_id = user.id
        except Exception as e:
            print(e)
            return Response(status=401)
        back = BackupRecord.objects.filter(id=back_id).first()
        if back:
            file_name_path = back.backup_filepath

            def file_iterator(file_name, chunk_size=512):
                with open(file_name, 'rb') as f:
                    while True:
                        c = f.read(chunk_size)
                        if c:
                            yield c
                        else:
                            break

            the_file_name = file_name_path
            print(escape_uri_path(file_name_path.split("/")[-1]))
            response = StreamingHttpResponse(file_iterator(the_file_name))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
                escape_uri_path(file_name_path.split("/")[-1]))

            return response
        else:
            return Response(status=401, data={'info': '无权限!'})


class TaskInfo(APIView):

    def post(self, request):
        resp = {
            'success': True,
            'info': '',
            'data': []
        }
        data = request.data
        task_id = data.get('task_id')
        task = Task.objects.filter(id=task_id).first()
        participate = json.loads(task.particpant)
        if task:
            host = Host.objects.filter(task=task)
            if host:
                masterAmount = Host.objects.filter(task=task).count()
                leakAmount = TaskVulnerability.objects.filter(task=task).count()
                voucherAmount = TaskCertificate.objects.filter(task=task).count()
                portAmount = TaskPort.objects.filter(task=task).count()
            else:
                masterAmount = 0
                leakAmount = 0
                voucherAmount = 0
                portAmount = 0
            fileAmount = FileDir.objects.filter(task=task).count()
            noteAmount = NoteDir.objects.filter(task=task).count()
            # process = task.task_process
            process_time = now() - task.start_time
            task_time = task.end_time - task.start_time
            process = process_time.days / task_time.days
            if process > 1:
                process = 1
            if process < 0:
                process = 0
            resp['data'] = {
                'id': task.id,
                'masterAmount': masterAmount,
                'createUser': task.user.name,
                'leakAmount': leakAmount,
                'portAmount': portAmount,
                'voucherAmount': voucherAmount,
                'fileAmount': fileAmount,
                'noteAmount': noteAmount,
                'process': f'{process * 100:.0f}',
                'mindLog': [],
                'noteLog': [],
                'fileLog': [],
                'title': task.title,
                'time': task.start_time.strftime('%Y/%m/%d') + "-" + task.end_time.strftime('%Y/%m/%d'),
                'description': task.description,
                'participate': [{'id': i, 'name': UserInfo.objects.get(id=i).name} for i in participate]

            }
            # 笔记日志:
            note_list = []
            noteLogs = NoteLog.objects.filter(task=task).order_by("-create_time")
            for noteLog in noteLogs:
                data = {
                    'name': noteLog.note_name,
                    'type': noteLog.action,
                    'user': UserInfo.objects.filter(id=noteLog.user_id).first().name,
                    'time': noteLog.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                note_list.append(data)
            if len(note_list) >= 10:
                note_list = note_list[0:9]
            else:
                note_list = note_list
            resp['data']['noteLog'] = note_list
            # 文件日志:
            file_list = []
            fileLogs = FileLog.objects.filter(task=task).order_by("-create_time")
            for fileLog in fileLogs:
                data = {
                    'name': fileLog.file_name,
                    'type': fileLog.action,
                    'user': UserInfo.objects.filter(id=fileLog.user_id).first().name,
                    'time': fileLog.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                file_list.append(data)
            if len(file_list) >= 10:
                file_list = file_list[0:9]
            else:
                file_list = file_list
            resp['data']['fileLog'] = file_list
            # 思维导图日志
            mind_list = []
            mindLogs = MindLog.objects.filter(task=task).order_by("-create_time")
            for mindLog in mindLogs:
                data = {
                    'name': mindLog.mind_name,
                    'type': mindLog.action,
                    'user': mindLog.user.name,
                    'time': mindLog.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                mind_list.append(data)
            if len(mind_list) >= 10:
                mind_list = mind_list[0:9]
            else:
                mind_list = mind_list
            resp['data']['mindLog'] = mind_list
            task_progress = TaskProgress.objects.filter(task=task).order_by('weight')
            timeLine = {"active": 0, "lineDet": []}
            for task_p in task_progress:
                time = ""
                if task_p.update_time:
                    timeLine["active"] += 1
                    time = task_p.update_time.strftime('%Y-%m-%d %H:%M:%S')
                    print(time)
                task_p_data = {
                    "title": task_p.name,
                    "time": time
                }
                timeLine["lineDet"].append(task_p_data)
            resp["data"]["timeLine"] = timeLine
        else:
            resp['success'] = False
            resp['info'] = '无此任务!'
        return Response(data=resp)


class HostList(APIView):

    def post(self, request):
        """查看主机列表"""
        resp = {
            'success': True,
            'data': [],
            'info': "",
            'total': 0
        }
        data = request.data
        task_id = data.get('id')
        search = data.get("search")
        page = int(data.get('page', 1))
        page_size = int(data.get('pageSize', 10))
        objs = Host.objects.filter(task_id=task_id)
        if search:
            objs = objs.filter(Q(ip__icontains=search) | Q(name__icontains=search))
        resp['total'] = objs.count()
        paginator = Paginator(objs, page_size)
        try:
            res_objs = paginator.page(page)
        except EmptyPage as e:
            print(e)
            resp['info'] = 'no more info'
            return Response(data=resp)
        ser_data = HostListSerializer(res_objs, many=True)
        resp['data'] = ser_data.data

        return Response(data=resp)


class HostView(APIView):

    @class_login_check
    def post(self, request):
        """新建主机"""
        resp = {
            'success': True,
            'info': '',
        }
        data = request.data
        user = request.myuser
        task_id = data.get('task_id')
        ips = data.get('ip')
        name = data.get("name")
        os_info = data.get('os_info')
        ip, port = check_ip(ips)
        task = Task.objects.filter(id=task_id).first()
        if not port:  # 如果ip后没跟开放端口
            Host.objects.create(name=name, os_info=os_info, ip=ip, task=task, user=user)
            resp['info'] = '新建主机成功!'
            task_progress(2, task_id)
            return Response(resp)
        else:
            ser_name = ServerPort.objects.filter(port=port).first()
            port_name = ser_name.server if ser_name else '未知'
            host = Host.objects.create(name=name, os_info=os_info, ip=ip, task=task, user=user)
            TaskPort.objects.create(name=port_name, port=port, host=host, task=task)
            task_progress(2, task_id)
            resp['info'] = '新建主机成功!'
        return Response(resp)

    @class_login_check
    def put(self, request):
        """编辑主机"""
        resp = {
            'success': True,
            'info': '',
        }

        data = request.data
        # user = request.myuser
        host_id = data.get("id")
        name = data.get("name")
        ips = data.get("ip")
        os_info = data.get("os_info")
        # ports = data.get("ports")
        ip, port_ = check_ip(ips)
        host = Host.objects.filter(id=host_id).first()
        try:
            if not port_:
                # try:
                # with transaction.atomic():
                host.name = name
                host.ip = ips
                host.os_info = os_info
                host.save()
            else:
                objs = TaskPort.objects.filter(port=port_, host__id=host.id, task=host.task).first()
                host.name = name
                host.ip = ip
                host.os_info = os_info
                host.save()
                ser_name = ServerPort.objects.filter(port=port_).first()
                port_name = ser_name.server if ser_name else '未知'
                if not objs:
                    TaskPort.objects.create(name=port_name, port=port_, host=host, task=host.task)
                else:
                    objs.name = port_name
                    objs.save()
            if host.node:
                mind_host = MindNode.objects.filter(id=host.node.id).first()
                mind_host.name = host.ip
                mind_host.os = host.os_info
                mind_host.save()
                # for port in ports:
            #     if (not port['name']) and (not port['port']):
            #         continue
            #     # 输入的ports里,port或者name有值
            #     obj = TaskPort.objects.filter(
            #         host__id=host.id, task=host.task).filter(
            #         Q(name=port["name"].upper()) | Q(port=port["port"])).first()
            #     print(obj)
            #     if not obj:
            #         if port["name"]:
            #             se_port = port_server.get(port["name"].upper())
            #             TaskPort.objects.create(name=port["name"].upper(),
            #                                     port=port["port"] if port["port"] else se_port, host=host,
            #                                     task=host.task)
            #         else:
            #             se_name = server_port.get(port["port"])
            #             TaskPort.objects.create(name=se_name, port=port["port"], host=host, task=host.task)
            #     else:
            #         if obj.name:
            #             obj.port = port["port"]
            #             obj.save()
            #         elif obj.port:
            #             obj.name = port["name"].upper() if port["name"] != '' else ''
            #             obj.save()
            # ex_ports = [p["name"] for p in ports]
            # for port in TaskPort.objects.filter(host__id=host.id):
            #     if port.name not in ex_ports:
            #         port.delete()
            resp['info'] = '编辑主机成功!'
            return Response(resp)
        except Exception as e:
            print(e)
            resp['success'] = False
            resp['info'] = '编辑主机失败!'

        return Response(resp)

    def delete(self, request):
        """删除主机"""
        resp = {
            'success': True,
            'info': ''
        }
        data = request.data
        id = data.get("id")
        host = Host.objects.filter(id=id).first()
        if host:
            try:
                with atomic():
                    vulners = TaskVulnerability.objects.filter(host=host)
                    certs = TaskCertificate.objects.filter(host=host)
                    ports = TaskPort.objects.filter(host=host)
                    for vulner in vulners:
                        vulner.delete()
                    for cert in certs:
                        cert.delete()
                    for port in ports:
                        port.delete()
                    host.delete()
                    resp['info'] = '主机删除成功!'
                    return Response(resp)
            except Exception as e:
                print(e)
                resp['success'] = False
                resp['info'] = '删除主机失败!'
                return Response(resp)
        else:
            resp['info'] = '主机不存在!'
            resp['success'] = False
        return Response(resp)


class HostPortListView(APIView):

    def get(self, request):
        """查看主机端口详情"""
        resp = {
            "success": True,
            "data": None,
            "info": ""
        }
        host_id = request.query_params.get("host_id")
        page = request.query_params.get('page')
        page_size = request.query_params.get('pageSize')
        search = request.query_params.get("search")
        ports = TaskPort.objects.filter(host__id=host_id)
        if search:
            ports = ports.filter(Q(name__icontains=search) | Q(port__icontains=search))
        ports = ports.all()
        if page and page_size:
            data_list = []
            for port in ports[(page - 1) * page_size: page * page_size]:
                data_list.append(
                    {"id": port.id, "name": port.name, "port": port.port, "name_disable": port.name != None})
            resp['total'] = ports.count()
            resp["data"] = data_list
        else:
            data_list = []
            for port in ports:
                data_list.append(
                    {"id": port.id, "name": port.name, "port": port.port, "name_disable": port.name != None})
            resp['total'] = ports.count()
            resp["data"] = data_list
        return Response(resp)

    def post(self, request):
        """新增端口信息"""
        resp = {
            'success': True,
            'data': [],
            'info': ''
        }
        host_id = request.data.get("host_id")
        name = request.data.get("name")
        name = name.upper()
        port = request.data.get("port")
        host = Host.objects.filter(id=host_id).first()
        taskPort = TaskPort.objects.filter(port=port, host=host).first()
        if not taskPort:
            if name and (not port):
                ser_port = ServerPort.objects.filter(server=name).first()
                port = ser_port.port if ser_port else None
            elif port and (not name):
                ser_name = ServerPort.objects.filter(port=port).first()
                name = ser_name.server if ser_name else '未知'
            elif port and name:
                pass
            TaskPort.objects.create(name=name, port=port, host=host, task=host.task)
            resp['info'] = '新增端口成功!'
        else:
            resp['success'] = False
            resp['info'] = '该端口已被占用!'
        return Response(resp)

    def put(self, request):
        """更新端口信息"""
        resp = {
            'success': True,
            'data': [],
            'info': ''
        }
        port_id = request.data.get("id")
        name = request.data.get("name")
        name = name.upper()
        port = request.data.get("port")
        taskPort = TaskPort.objects.filter(id=port_id).first()
        if taskPort:
            if name and (not port):
                ser_port = ServerPort.objects.filter(server=name).first()
                port_ = ser_port.port if ser_port else None
                taskPort.port = port_
                taskPort.save()
            elif port and (not name):
                ser_name = ServerPort.objects.filter(port=port).first()
                port_name = ser_name.server if ser_name else '未知'
                taskPort.name = port_name
                taskPort.save()
            elif port and name:
                taskPort.name = name
                taskPort.port = port
                taskPort.save()
            resp['info'] = '更新端口成功!'
        else:
            resp['info'] = '端口信息获取失败!'
            resp['success'] = False
        return Response(resp)

    def delete(self, request):
        """删除端口信息"""
        resp = {
            'success': True,
            'data': [],
            'info': ''
        }
        port_id = request.data.get('id')
        taskPort = TaskPort.objects.filter(id=port_id).first()
        if taskPort:
            taskPort.delete()
            resp['info'] = '删除端口成功!'
        else:
            resp['success'] = False
            resp['info'] = '端口信息不存在!'
        return Response(resp)


class VulnerabilityListView(APIView):

    def get(self, request):
        """查看漏洞列表"""
        resp = {
            "data": None,
            "success": True,
            "info": "",
            "total": 0
        }
        task_id = request.query_params.get("id")
        search = request.query_params.get("search")
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 10))
        host_search = int(request.query_params.get('host_search') or 0)
        data = list()

        vulners = TaskVulnerability.objects.filter(task__id=task_id)
        if host_search:
            vulners = vulners.filter(host__id=host_search)
        if search:
            vulners = vulners.filter(name__icontains=search)
        vulners = vulners.all()
        for vulner in vulners[(page - 1) * page_size: page * page_size]:
            data.append({
                "id": vulner.id,
                "name": vulner.name,
                "describe": vulner.describe,
                "quote": vulner.quote,
                "host": vulner.host.ip,
                "level": vulner.level,
                "user": vulner.user.name,
                "create_time": vulner.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        resp['total'] = vulners.count()
        resp['data'] = data
        return Response(resp)


class VulnerabilityView(APIView):

    @class_login_check
    def post(self, request):
        """新建/修改漏洞"""
        data = request.data
        user = request.myuser
        id = data.get("id")
        name = data.get("name")
        describe = data.get("description")
        quote = data.get("quote")
        level = data.get("level")
        host = Host.objects.filter(id=data.get("host_id")).first()
        print(name, describe, quote, level, host)
        if not all((name, describe, quote, level is not None, host)):
            return Response({"success": False, "info": "参数不全"})
        if id:
            try:
                with transaction.atomic():
                    vulner = TaskVulnerability.objects.filter(id=id).first()
                    vulner.name = name
                    vulner.describe = describe
                    vulner.quote = quote
                    vulner.level = level
                    vulner.host = host
                    vulner.save()
                return Response({"success": True, "info": "编辑漏洞成功"})
            except Exception as e:
                print('err:', e)
                return Response({"success": False, "info": "编辑漏洞失败"})
        else:
            TaskVulnerability.objects.create(name=name, describe=describe, quote=quote, level=level,
                                             host=host, user=user,
                                             task=host.task)
            task_progress(3, host.task.id)

        return Response({"success": True, "info": "创建漏洞成功"})

    def delete(self, request):
        """删除漏洞"""
        resp = {
            'success': True,
            'info': ''
        }
        data = request.data
        id = data.get("id")
        vulner = TaskVulnerability.objects.filter(id=id).first()
        if vulner:
            vulner.delete()
            resp['info'] = '漏洞删除成功!'
        else:
            resp['info'] = '漏洞不存在!'
            resp['success'] = False
        return Response(resp)


class CertificateListView(APIView):

    def get(self, request):
        """查看凭证列表"""
        resp = {
            "data": None,
            "success": True,
            "info": "",
            "total": 0
        }

        task_id = request.query_params.get("id")
        search = request.query_params.get("search")
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 10))
        host_search = int(request.query_params.get('host_search') or 0)

        if not task_id:
            resp['success'] = False
            resp['info'] = "没有task"
            return Response(resp)
        data = list()

        certs = TaskCertificate.objects.filter(task__id=task_id)
        if host_search:
            certs = certs.filter(host__id=host_search)
        if search:
            certs = certs.filter(Q(name__icontains=search) | Q(user__name__icontains=search))
        certs = certs.all()
        for cert in certs[(page - 1) * page_size: page * page_size]:
            data.append({
                "id": cert.id,
                "name": cert.name,
                "ip": cert.host.ip,
                "user": cert.user.name,
                "username": cert.username,
                "password": cert.password,
            })
        host_ips = [{"id": h.id, "ip": h.ip} for h in Host.objects.filter(task__id=task_id).all()]
        resp['data'] = data
        resp['total'] = certs.count()
        resp['host_ips'] = host_ips
        return Response(resp)


class CertificateView(APIView):

    @class_login_check
    def post(self, request):
        """新建/修改凭证"""
        data = request.data
        user = request.myuser
        id = data.get("id")
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")
        host = Host.objects.filter(id=data.get("host_id")).first()
        if not all((name, username, password, host)):
            return Response({"success": False, "info": "参数不全"})
        if id:
            try:
                with transaction.atomic():
                    cert = TaskCertificate.objects.filter(id=id).first()
                    cert.name = name
                    cert.username = username
                    cert.password = password
                    cert.host = host
                    cert.save()
                return Response({"success": True, "info": "编辑凭证成功"})
            except Exception as e:
                print('err:', e)
                return Response({"success": False, "info": "编辑凭证失败"})
        else:
            if not user:
                return Response({"success": False, "info": "参数不全!!"})
            TaskCertificate.objects.create(name=name, username=username, user=user, password=password,
                                           host=host, task=host.task)
            task_progress(4, host.task.id)
        return Response({"success": True, "info": "创建凭证成功"})

    def delete(self, request):
        """删除凭证"""
        resp = {
            'success': True,
            'info': ''
        }
        data = request.data
        id = data.get("id")
        cert = TaskCertificate.objects.filter(id=id).first()
        if cert:
            cert.delete()
            resp['info'] = '凭证删除成功!'
        else:
            resp['info'] = '凭证不存在!'
            resp['success'] = False
        return Response(resp)
