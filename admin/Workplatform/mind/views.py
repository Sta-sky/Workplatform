import ipaddress

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from adminq.models import Host, TaskPort, ServerPort
from mind.utils import NoteLock, check_node_name, update_mind, check_node_lock, request_zoomeye_api, create_note, \
    get_region, task_progress, get_dir
from taskmanage.models import NoteDir, Label, Note, File
from util.logging_checked import class_login_check
from .serializers import MindTreeSerializer
from .models import MindMap, MindOnlineUser, MindNode, OpenDir, NodeFile, MindLog, MindNodeLog


class MindView(APIView):
    """
    get:思维导图列表
    post: 思维导图详情
    delete:思维导图删除
    """

    @class_login_check
    def get(self, request):
        """

        """
        task_id = request.query_params.get("task_id")
        search = request.query_params.get("search")
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        if task_id:
            mind_maps = MindMap.objects.filter(task_id=task_id, title__contains=search)
            pagetor = Paginator(mind_maps, page_size)
            current_info_list = pagetor.page(page)
            data_list = []
            for mind_map in current_info_list:
                data = {
                    "title": mind_map.title,
                    "description": mind_map.description,
                    "create_time": mind_map.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "user": mind_map.user.name,
                    "id": mind_map.id
                }
                data_list.append(data)
            data = {
                "success": True,
                "count": mind_maps.count(),
                "data": data_list

            }
            return Response(data=data)
        else:
            return Response({"success": False, "info": "参数错误！"})

    @class_login_check
    def delete(self, request):
        mind_id = request.data.get("mind_id")
        user = request.myuser
        if mind_id:
            mind = MindMap.objects.filter(id=mind_id).first()
            if mind:
                if mind.user == user or user.user_permission:
                    mind.delete()
                    """
                    action = models.IntegerField(verbose_name='执行动作', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    mind_name = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
                    """
                    MindLog.objects.create(action=3, mind_name=mind.title, user=user, task=mind.task)
                    return Response({"success": True, "info": ""})
                else:
                    return Response({"success": False, "info": "权限错误！"})
            else:
                return Response({"success": False, "info": "参数错误！"})
        else:
            return Response({"success": False, "info": "参数错误！"})

    @class_login_check
    def post(self, request):
        mind_id = request.data.get("mind_id")
        user = request.myuser
        if mind_id:
            try:
                mind = MindMap.objects.get(id=mind_id)
            except Exception as e:
                return Response({"success": False, "info": ""})
            # 递归获取数据
            mind_note = MindNode.objects.filter(mind=mind)
            content = MindTreeSerializer(mind_note, many=True)
            users = MindOnlineUser.objects.filter(mind=mind)
            online_list = []
            for i in users:
                user_data = {
                    "username": i.user.name,
                }
                online_list.append(user_data)
            if not users.filter(user=user):
                MindOnlineUser.objects.create(mind=mind, user=user)
                # todo 所有的在线人员广播同步
                online_list.append({"username": user.name})
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f"online_{mind_id}",
                                                    {"type": "chat2.message", "message": online_list})
            data = {
                "title": mind.title,
                "user": mind.user.name,
                "online_list": online_list,
                "content": content.data
            }
            return Response({"success": True, "data": data})


class MindCreate(APIView):
    @class_login_check
    def post(self, request):
        """
        title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
        :param request:
        :return:
        """
        title = request.data.get("title")
        description = request.data.get("description")
        task_id = request.data.get("task_id")
        user = request.myuser
        if title and task_id:
            # 创建思维导图
            mind = MindMap.objects.create(title=title, description=description, task_id=task_id, user=user)
            task_progress(2, task_id)
            # 创建第一个节点
            MindNode.objects.create(mind=mind, name=title, node_type=4, left=False)
            MindLog.objects.create(action=1, mind_name=mind.title, user=user, task=mind.task)
            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": ""})


class MindDisconnect(APIView):
    @class_login_check
    def post(self, request):
        mind_id = request.data.get("mind_id")
        user = request.myuser
        channel_layer = get_channel_layer()
        MindOnlineUser.objects.filter(user=user, mind_id=mind_id).delete()
        users = MindOnlineUser.objects.filter(mind_id=mind_id)
        online_list = []
        for i in users:
            user_data = {
                "username": i.user.name,
            }
            online_list.append(user_data)
        async_to_sync(channel_layer.group_send)(f"online_{mind_id}",
                                                {"type": "chat2.message", "message": online_list})
        return Response({"success": True, "info": ""})


class MindNodeView(APIView):
    @class_login_check
    def post(self, request):
        # 新增节点
        task_id = request.data.get("task_id")
        mind_id = request.data.get("mind_id")
        parent_id = request.data.get("parent_id")
        left = request.data.get("left")
        name = request.data.get("name")
        index = request.data.get("index")
        # 校验是否是ip
        node_type = 4
        # 查询这个父节点下所有的子节点
        mind_node = MindNode.objects.filter(child_id=parent_id, index__gte=index).order_by("index")
        for i in mind_node:
            i.index += 1
            i.save()
        mind = MindNode.objects.create(name=name, node_type=node_type, left=left, child_id=parent_id, index=index)
        MindNodeLog.objects.create(action=1, user=request.myuser, mind_id=mind_id, node_name=mind.name)

        node_type = check_node_name(name, mind, task_id, request)
        mind.node_type = node_type
        mind.save()
        update_mind(mind_id, "")
        return Response({"success": True, "info": "", "node_id": mind.id})

    @class_login_check
    def put(self, request):
        mind_id = request.data.get("mind_id")
        task_id = request.data.get("task_id")
        name = request.data.get("name")
        node_id = request.data.get("node_id")
        left = request.data.get("left")
        index = request.data.get("index")
        mind_node = MindNode.objects.filter(id=node_id).first()
        if name and mind_node:

            # TaskPort.objects.filter(node_id=node_id).delete()
            # OpenDir.objects.filter(node_id=node_id).delete()
            # 修改后
            l = 1
            if index != mind_node.index:
                mind_nodes = MindNode.objects.filter(child=mind_node.child, index__gt=index).order_by("index")
                for i in mind_nodes:
                    i.index = index + l
                    i.save()
                    l += 1
            node_type = check_node_name(name, mind_node, task_id, request)
            if name != mind_node.name:
                mind_node.name = name
            mind_node.index = index
            mind_node.node_type = node_type
            mind_node.left = left
            mind_node.save()
            # todo info
            update_mind(mind_id, "")
            MindNodeLog.objects.create(action=2, user=request.myuser, mind_id=mind_id, node_name=mind_node.name)

            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": "节点不能为空"})

    @class_login_check
    def delete(self, request):
        mind_id = request.data.get("mind_id")
        node_id = request.data.get("node_id")
        if mind_id and node_id:
            is_delete = check_node_lock(node_id=node_id)
            if is_delete:
                node = MindNode.objects.filter(id=node_id).first()

                MindNodeLog.objects.create(action=3, user=request.myuser, mind_id=mind_id, node_name=node.name)
                node.delete()
                update_mind(mind_id, "")
                MindNodeLog.objects.create(action=3, user=request.myuser, mind_id=mind_id, node_name=node.name)

                return Response({"success": True, "info": ""})
            else:
                return Response({"success": False, "info": "有节点正在被他人编辑请稍后删除！"})
        else:
            return Response({"success": False, "info": ""})


class LockNode(APIView):
    @class_login_check
    def put(self, request):
        user = request.myuser
        node_id = request.data.get("node_id")
        is_lock = NoteLock(node_id).get_node_lock_redis()
        if not is_lock:
            return Response({"success": False, "info": ""})
        else:
            if is_lock.decode() == user.name:
                return Response({"success": False, "info": ""})
        return Response({"success": True, "info": ""})

    @class_login_check
    def post(self, request):
        # 锁定节点
        user = request.myuser
        node_id = request.data.get("node_id")
        is_lock = NoteLock(node_id).get_node_lock_redis()
        if not is_lock:
            NoteLock(node_id).set_lock(user.name)
        return Response({"success": True, "info": ""})

    @class_login_check
    def delete(self, request):
        user = request.myuser
        node_id = request.data.get("node_id")
        is_delete = NoteLock(node_id).delete_lock(user.name)
        if is_delete:
            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": "解锁失败！"})


class NodeDetail(APIView):
    @class_login_check
    def post(self, request):
        user = request.myuser
        node_id = request.data.get("node_id")
        if node_id:
            is_lock = NoteLock(node_id).get_node_lock_redis()
            try:
                is_lock = is_lock.decode()
                print(is_lock)
            except:
                is_lock = None
            if not is_lock or is_lock == user.name:
                NoteLock(node_id).set_lock(user.name)
                node = MindNode.objects.get(id=node_id)
                data = {
                    "name": node.name,
                    "os": node.os,
                    "node_type": node.node_type,
                    "ascription": node.ascription,
                    "note": node.note,
                    "port": [],
                    "dir": get_dir(1, 5, node_id),
                    "file": []
                }
                file = node.nodefile_set.all()
                for i in file:
                    data["file"].append({"name": i.file.file_name, "id": i.file.id})
                dir_list = node.opendir_set.all()[0:10]

                for i in dir_list:
                    data["dir"].append(i.dir)
                port_list = node.taskport_set.all()[0:10]
                for i in port_list:
                    data["port"].append({"name": i.name, "port": i.port})
                return Response({"success": True, "info": "", "data": data})
            else:
                return Response({"success": False, "info": f"用户 {is_lock} 正在编辑此节点，请稍后重试！"})
        else:
            return Response({"success": False, "info": ""})


class HostListView(APIView):
    @class_login_check
    def post(self, request):
        node_id = request.data.get("node_id")
        if node_id:
            host_list = Host.objects.filter(node_id=node_id)
            data_list = []
            for i in host_list:
                data_list.append({"ip": i.ip, "id": i.id})
            return Response({"success": True, "data": data_list})
        else:
            return Response({"success": False, "data": []})


class PortListView(APIView):
    @class_login_check
    def get(self, request):
        host_id = request.query_params.get("host_id")
        node_id = request.query_params.get("node_id")
        page = request.query_params.get("page")
        page_size = request.query_params.get("page_size")
        if node_id:
            node_id = int(node_id)
            if host_id:
                host_id = int(host_id)
                host = Host.objects.get(id=host_id)
                port_list = TaskPort.objects.filter(host=host, node_id=node_id)
            else:

                port_list = TaskPort.objects.filter(node_id=node_id)
            pagetor = Paginator(port_list, page_size)
            current_info_list = pagetor.page(page)
            data_list = []
            for i in current_info_list:
                data_list.append({
                    "id": i.id,
                    "name": i.name,
                    "port": i.port,
                    "ip": i.host.ip
                })
            return Response({"success": True, "count": port_list.count(), "data": data_list})
        else:
            return Response({"success": False, "info": "参数错误!"})

    @class_login_check
    def post(self, request):
        port = request.data.get("port")
        port_name = request.data.get("port_name")
        ip = request.data.get("ip")
        task_id = request.data.get("task_id")
        node_id = request.data.get("node_id")
        if ip:
            try:
                ipaddress.ip_network(ip)
                host = Host.objects.filter(node_id=node_id, ip=ip).first()
                if not host:
                    host = Host.objects.create(node_id=node_id, ip=ip, task_id=task_id, user=request.myuser)
            except:
                return Response({"success": False, "info": "ip 填写错误！"})
            name = port_name.upper()
            taskPort = TaskPort.objects.filter(port=port, host=host).first()
            if not taskPort:
                if name and (not port):
                    ser_port = ServerPort.objects.filter(server=name).first()
                    if ser_port:
                        port = ser_port.port
                    else:
                        port = None
                elif port and (not name):
                    ser_name = ServerPort.objects.filter(port=port).first()
                    if ser_name:
                        port_name = ser_name.server
                    else:
                        port_name = '未知'
            else:
                return Response({"success": False, "info": "端口已经存在"})
            TaskPort.objects.create(name=port_name, host=host, task_id=task_id, port=port, node_id=node_id)
            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": "参数错误！"})

    @class_login_check
    def delete(self, request):
        port_id = request.data.get("port_id")
        if port_id:
            TaskPort.objects.filter(id=port_id).delete()
            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": "参数错误！"})


class PortScan(APIView):

    def post(self, request):
        node_id = request.data.get("node_id")
        if node_id:
            mind_node = MindNode.objects.filter(id=node_id).first()
            if mind_node:
                if mind_node.node_type == 1:
                    # 使用zoomeye进行数据获取
                    data = request_zoomeye_api("176.12.12.1", 1, 1)
                    if data["total"] >= 1:
                        ip_data = data["data"][0]

                    return Response(data)
                elif mind_node.node_type == 2:
                    # 使用
                    pass
                elif mind_node.node_type == 3:
                    # zoomeye
                    pass
                else:
                    return Response({"success": True, "info": "目前暂不支持这类型的节点进行端口获取！"})
            else:
                return Response({"success": False, "info": "参数错误！"})
        else:
            return Response({"success": False, "info": "参数错误！"})


class CreateNote(APIView):
    @class_login_check
    def post(self, request):
        mind_id = request.data.get("mind_id")
        task_id = request.data.get("task_id")
        node = MindNode.objects.filter(mind_id=mind_id).first()
        note_data = "#" + node.name + "\n\r" + "\t" + node.note if node.note else "" + "\n\n\n"
        node_id = node.id
        data, _ = create_note(node_id, note_data)
        # 创建新的笔记
        note_dir = NoteDir.objects.filter(task_id=task_id, is_primary_dir=True)
        note_dir_id = 0
        for dir in note_dir:
            if dir.file_name == "思维导图":
                note_dir_id = dir.id
        if not note_dir_id:
            note_dir_id = NoteDir.objects.create(file_name="思维导图", is_primary_dir=True, task_id=task_id).id

        # 创建笔记
        label = Label.objects.filter(label_name="思维导图").first()
        if label:
            label_id = label.id
        else:
            label_id = Label.objects.create(label_name="思维导图").id
        """
    note_name = models.CharField(max_length=1000, verbose_name='笔记名')
    content = models.TextField(verbose_name='笔记内容', null=True)
    note_premission = models.IntegerField(verbose_name='笔记权限', default=2)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    classify = models.IntegerField(default=1, verbose_name='笔记分类')
    label = models.ForeignKey(Label, verbose_name='笔记标签', on_delete=models.CASCADE)
    file_dir = models.ForeignKey(NoteDir, verbose_name='归属目录', on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, verbose_name='创建人', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='对应任务', on_delete=models.CASCADE)
        """
        Note.objects.create(note_name=node.name, content=data, classify=2, label_id=label_id, user=request.myuser,
                            task_id=task_id, file_dir_id=note_dir_id)
        return Response(data={"success": True, "info": ""})


class NoteFileView(APIView):

    def get(self, request):
        task_id = request.query_params.get("task_id")

        file_list = File.objects.filter(task_id=task_id)
        data_list = []
        for i in file_list:
            data_list.append({"name": i.file_name, "id": i.id})
        return Response({"success": True, "data": data_list})

    def post(self, request):
        file_id_list = request.data.get("file_id_list")
        node_id = request.data.get("node_id")

        model_file_list = [file.id for file in NodeFile.objects.filter(node_id=node_id)]

        if file_id_list != model_file_list:
            intersect_list = list(set(file_id_list).intersection(set(model_file_list)))
            delete_list = list(set(intersect_list) ^ set(model_file_list))
            update_list = list(set(intersect_list) ^ set(file_id_list))
            if delete_list:
                NodeFile.objects.filter(id__in=delete_list).delete()
            if update_list:
                for i in update_list:
                    NodeFile.objects.create(node_id=node_id, file_id=i)
        return Response({"success": True, "info": ""})


class EMindLog(APIView):

    def get(self, request):
        task_id = request.query_params.get("task_id")
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        if task_id:
            mind_maps = MindLog.objects.filter(task_id=task_id)
            pagetor = Paginator(mind_maps, page_size)
            current_info_list = pagetor.page(page)
            data_list = []
            for mind_map in current_info_list:
                data = {
                    "action": mind_map.action,
                    "create_time": mind_map.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "user": mind_map.user.name,
                    "id": mind_map.id,
                    "mind_name": mind_map.mind_name
                }
                data_list.append(data)
            data = {
                "success": True,
                "count": mind_maps.count(),
                "data": data_list

            }
            return Response(data=data)
        else:
            return Response({"success": False, "info": "参数错误！"})


class MindLogView(APIView):

    def get(self, request):
        mind_id = request.query_params.get("mind_id")
        page_size = request.query_params.get("page_size")
        page = request.query_params.get("page")
        if mind_id:
            mind_maps = MindNodeLog.objects.filter(mind_id=mind_id)
            pagetor = Paginator(mind_maps, page_size)
            current_info_list = pagetor.page(page)
            data_list = []
            for mind_map in current_info_list:
                data = {
                    "action": mind_map.action,
                    "create_time": mind_map.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "user": mind_map.user.name,
                    "id": mind_map.id,
                    "node_name": mind_map.node_name,
                    "mind_name": mind_map.mind.title
                }
                data_list.append(data)
            data = {
                "success": True,
                "count": mind_maps.count(),
                "data": data_list

            }
            return Response(data=data)
        else:
            return Response({"success": False, "info": "参数错误！"})


class NoteView(APIView):

    def post(self, request):
        node_id = request.data.get("node_id")
        note = request.data.get("note")
        if note and node_id:
            MindNode.objects.filter(id=node_id).update(note=note)
            return Response({"success": True, "info": ""})
        else:
            return Response({"success": False, "info": "参数错误！"})
