# -*- coding: utf-8 -*-
import json
import os
import uuid

from urllib.parse import quote

from django.http import JsonResponse, FileResponse, HttpResponse
from django.views import View

from Workplatform import settings
from adminq.models import TaskProgress
from mind.utils import task_progress
from taskmanage.utils import write_sys_log, handle_repet_name, delete_note_image, MarkdownPdf
from util.logging_checked import class_login_check, def_login_check, token_return_user
from util.redis_connect import Redis
from util.response_code import code
from util.util import judge_data_complate, save_imgage
from taskmanage.models import Task, Note, NoteDir, File, FileDir, Label, BackNote, NoteLog, FileLog


class CreateDeleteTask(View):
    """
    post : 创建任务
    get  : 删除任务
    """

    @class_login_check
    def post(self, request):
        body_data = request.body
        user = request.myuser
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[60004])
        try:
            task = Task().create_task(data, user)
            # 插入任务进度
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
            for k, v in progress_dict.items():
                TaskProgress.objects.create(name=v, weight=k, task=task)
            user.task_count += 1
            user.save()
            action_info = f'创建任务: [{data.get("title")}]'
            write_sys_log(action_info, user)
            CreateDeleteTask().del_user_info_cache()
        except Exception:
            return JsonResponse(code[20002])
        return JsonResponse(code[200])

    @class_login_check
    def get(self, request):
        task_id = request.GET.get('task_id')
        user = request.myuser
        try:
            task_obj = Task.objects.get(id=task_id)
            if user.user_permission == 1 or task_obj.user_id == user.id:
                result = Task().delete_task(task_id)
                action_info = f'删除任务: [{task_obj.title}]'
                write_sys_log(action_info, user)
                if not result:
                    return JsonResponse(code[20006])
                CreateDeleteTask().del_user_info_cache()
                return JsonResponse(code[200])
            return JsonResponse(code[20009])
        except Exception:
            return JsonResponse(code[20006])

    @classmethod
    def del_user_info_cache(cls):
        redis_obj = Redis('user')
        redis_obj.redis_delete('user_info')
        redis_obj.redis_delete('all_user_info')


class QueryModifyTask(View):
    """
    post : 修改任务
    get  : 查询任务
    """

    @class_login_check
    def get(self, request):
        page = request.GET.get('page')
        max_count = request.GET.get('max_count')
        search_word = request.GET.get('keyword')
        user = request.myuser
        try:
            data, page_num, task_permission = Task().query_all_task(page, max_count, search_word, user)
            res_data = code[200]
            res_data['data'] = data
            res_data['total'] = page_num
            res_data['task_permission'] = task_permission
        except Exception as e:
            err_info = code[60003]
            err_info['info'] = str(e)
            return JsonResponse(err_info)
        return JsonResponse(res_data)

    @class_login_check
    def post(self, request):
        user = request.myuser
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[60004])
        try:
            result = Task().modify_task(data)
            if not result:
                return JsonResponse(code[20003])
        except Exception as e:
            err_info = code[60003]
            err_info['info'] = str(e)
            return JsonResponse(err_info)
        action_info = f'修改任务: [{data.get("title")}]'
        write_sys_log(action_info, user)
        return JsonResponse(code[200])


def task_detail(request):
    """
    任务详情展示页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        task_id = request.GET.get('task_id')
        flag, result_dic = Task().query_task_detail(task_id)
        if not flag:
            return JsonResponse(code[20003])
        res_data = code[200]
        res_data['data'] = result_dic
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


class AddSubDir(View):
    """
    post: 增加文件子目录
    get : 删除目录
    """

    def post(self, request):
        data = judge_data_complate(request.body)
        if not data:
            return JsonResponse(code[60004])
        try:
            res = NoteDir().create_dir(data)
            if not res:
                return JsonResponse(code[30001])
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            return JsonResponse(code[20003])

    @class_login_check
    def get(self, request):
        dir_id = request.GET.get('dir_id')
        try:
            user = request.myuser
            dirs = NoteDir.objects.get(id=dir_id)
            pid = dirs.pid
            if pid:
                primery_dir = NoteDir.objects.get(id=pid)
                sub_str = primery_dir.sub_dir
                primery_dir.sub_dir = self.handle_sub_dir_str(sub_str, dir_id)
                primery_dir.save()
            self.delete_dir(dir_id, user)
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            return JsonResponse(code[30002])

    @classmethod
    def handle_sub_dir_str(cls, sub_dir, p_id):
        if not sub_dir:
            return None
        sub_str = sub_dir.split('_')
        sub_str.remove(str(p_id))
        str_sub = '_'.join(sub_str)
        return str_sub

    def delete_dir(self, dir_id, user):
        """ 删除目录 """
        try:
            dir_obj = NoteDir.objects.get(id=dir_id)
            sub_dir = dir_obj.sub_dir
            note = Note.objects.filter(file_dir_id=dir_id)
            for info in note:
                note.delete()
                NoteLog().write_note_action_log(3, info.note_name, user.id, dir_obj.task_id)
            NoteDir.objects.get(id=dir_id).delete()
            if sub_dir:
                sub_dir = sub_dir.split('_')
                for dirs in sub_dir:
                    print(f'当前删除的目录为{dirs}')
                    self.delete_dir(int(dirs), user)
        except Exception as e:
            print(e)
            raise


class ModifyQueryDir(View):
    """
    post: 修改目录
    get : 查询目录详情
    """

    def post(self, request):
        data = judge_data_complate(request.body)
        if not data:
            return JsonResponse(code[60004])
        try:
            NoteDir().modify_dir_name(data)
            return JsonResponse(code[200])
        except Exception:
            return JsonResponse(code[20003])

    def get(self, request):
        task_id = request.GET.get('task_id')
        is_primary = int(request.GET.get('is_primary'))
        dir_id = request.GET.get('dir_id')
        page = request.GET.get('page')
        max_count = request.GET.get('max_count')
        print(f'目录， is_primary, 任务id{dir_id, is_primary, task_id}')
        try:
            result = Note().query_file_dir(task_id, page, max_count, is_primary, dir_id)
            res_data = code[200]
            res_data['data'] = result
            return JsonResponse(res_data)
        except Exception:
            return JsonResponse(code[20008])


@def_login_check
def edit_note(request):
    """
    笔记编辑， 点击后redis加锁
    """
    if request.method == 'GET':
        try:
            task_id = int(request.GET.get('task_id'))
            note_id = request.GET.get('note_id')
            flag = int(request.GET.get('flag'))
            user = request.myuser
            task = Task.objects.get(id=task_id)
            particpant = json.loads(task.particpant)
            if user.id not in particpant and not user.user_permission:
                return JsonResponse(code[40012])
            redis_obj = Redis('note')
            if flag:
                flag, result = redis_obj.acquire_lock(note_id)
                if flag:
                    return JsonResponse(code[200])
                return JsonResponse(code[40010])
            else:
                redis_obj.delete_lock(note_id)
                return JsonResponse(code[40011])
        except Exception as e:
            return JsonResponse(code[20007])
    else:
        return JsonResponse(code[60001])


class AddDelNote(View):
    """
    post : 添加笔记
    get  : 删除笔记
    """

    @class_login_check
    def post(self, request):
        data = judge_data_complate(request.body)
        user = request.myuser
        if not data:
            return JsonResponse(code[60004])
        try:
            flag, task_id = Note().add_note(data, user)
            if not flag:
                return JsonResponse(code[40002])
            task_progress(6, task_id)
        except Exception:
            return JsonResponse(code[40001])
        return JsonResponse(code[200])

    @class_login_check
    def get(self, request):
        try:
            note_id = request.GET.get('note_id')
            user = request.myuser
            result = AddDelNote().delete_note(note_id, user)
            if not result:
                return JsonResponse(code[40007])
            return JsonResponse(code[200])
        except Exception as e:
            return JsonResponse(code[40007])

    @classmethod
    def delete_note(cls, note_id, user):
        """note_id  删除笔记"""
        try:
            note = Note.objects.get(id=note_id)
            note_dir = NoteDir.objects.get(id=note.file_dir.id)
            content = note.content
            delete_note_image(content)
            task_id = note_dir.task_id
            note.delete()
            BackNote().note_id_delete(note_id)
            if note.note_premission == 2:
                action_info = f'删除笔记: [{note_dir.note_name}]'
                write_sys_log(action_info, user)
            NoteLog().write_note_action_log(3, note.note_name, user.id, task_id)
            return True
        except Exception as e:
            return False


class ModifyqueryNot(View):
    """
    post : 修改笔记
    get  : 查询笔记
    """

    @class_login_check
    def post(self, request):
        user = request.myuser
        data = judge_data_complate(request.body)
        if not data:
            return JsonResponse(code[60004])
        try:
            result = Note().modify_note(data, user)
            if not result:
                return JsonResponse(code[40004])
        except Exception as e:
            print(e)
            return JsonResponse(code[40005])
        return JsonResponse(code[200])

    def get(self, request):
        note_id = request.GET.get('note_id')
        try:
            data_dic = Note().query_note_info(note_id)
            res_data = code[200]
            res_data['data'] = data_dic.get('data', '')
        except Exception:
            return JsonResponse(code[40005])
        return JsonResponse(res_data)


class AddDelDir(View):
    """
    post: 增加文件子目录
    get : 删除目录
    """

    def post(self, request):
        data = judge_data_complate(request.body)
        if not data:
            return JsonResponse(code[60004])
        try:
            res = FileDir().create_dir(data)
            if not res:
                return JsonResponse(code[30001])
            return JsonResponse(code[200])
        except Exception:
            return JsonResponse(code[20003])

    @class_login_check
    def get(self, request):
        """
        删除dir_id:
            1、更新父目录中的子目录字段
        """
        dir_id = request.GET.get('dir_id')
        user = request.myuser
        try:
            dirs = FileDir.objects.get(id=dir_id)
            pid = dirs.pid
            if pid:
                primery_dir = FileDir.objects.get(id=pid)
                sub_str = primery_dir.sub_dir
                primery_dir.sub_dir = self.handle_sub_dir_str(sub_str, dir_id)
                primery_dir.save()
            self.delete_dir(dir_id, user)
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            return JsonResponse(code[30002])

    @classmethod
    def handle_sub_dir_str(cls, sub_dir, p_id):
        if not sub_dir:
            return None
        sub_str = sub_dir.split('_')
        sub_str.remove(str(p_id))
        str_sub = '_'.join(sub_str)
        settings.SUB_TASK_LIST = []
        return str_sub

    def delete_dir(self, dir_id, user):
        """删除目录"""
        try:
            dir_obj = FileDir.objects.get(id=dir_id)
            sub_dir = dir_obj.sub_dir
            file = File.objects.filter(file_dir=dir_id)
            for info in file:
                FileLog().write_file_action_log(3, user.id, info.file_name, dir_obj.task_id)
            dir_obj.delete()
            file.delete()
            if sub_dir:
                sub_dir = sub_dir.split('_')
                for dirs in sub_dir:
                    self.delete_dir(int(dirs), user)
        except Exception as e:
            raise


class ModifyQueryFileDir(View):
    """
    post: 修改目录
    get : 查询目录详情
    """

    def post(self, request):
        data = judge_data_complate(request.body)
        if not data:
            return JsonResponse(code[60004])
        try:
            FileDir().modify_dir_name(data)
            return JsonResponse(code[200])
        except Exception:
            return JsonResponse(code[20003])

    def get(self, request):
        task_id = request.GET.get('task_id')
        is_primary = int(request.GET.get('is_primary'))
        dir_id = request.GET.get('dir_id')
        page = request.GET.get('page')
        max_count = request.GET.get('max_count')
        try:
            Task.objects.get(id=task_id)
        except Exception as e:
            return JsonResponse(code[20003])
        try:
            result = File().query_file_dir(task_id, page, max_count, is_primary, dir_id)
            res_data = code[200]
            res_data['data'] = result
            return JsonResponse(res_data)
        except Exception as e:
            print(e)
            return JsonResponse(code[20003])


class AddDelFile(View):
    """
    post : 添加文件
    get  : 删除文件
    """

    @class_login_check
    def post(self, request):
        user = request.myuser
        pid = request.POST.get('p_dir_id')
        description = request.POST.get('description')
        myfile = request.FILES.get('file')
        file_name = myfile.name
        save_path, name_file = handle_repet_name(file_name)
        save_path = AddDelFile().parse_file(myfile, save_path)
        try:
            flag, task_id = File().add_file(pid, description, name_file, save_path, user)
            if not flag:
                return JsonResponse(code[30003])
            task_progress(6, task_id)
            print('文件进入写入完成')
        except Exception:
            return JsonResponse(code[30003])
        return JsonResponse(code[200])

    @class_login_check
    def get(self, request):
        try:
            user = request.myuser
            file_id = request.GET.get('file_id')
            file = File.objects.get(id=file_id)
            task_id = file.file_dir.task_id
            save_path = file.file_path
            File.objects.filter(id=file_id).delete()
            if os.path.exists(save_path):
                os.remove(save_path)
            FileLog().write_file_action_log(3, user.id, file.file_name, task_id)
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            return JsonResponse(code[40007])

    @classmethod
    def parse_file(cls, myfile, save_file_path):
        destination = open(save_file_path, 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()
        print('文件上传完成')
        return save_file_path


@def_login_check
def uploade_notes(request):
    """批量文件上传"""
    if request.method == 'POST':
        try:
            task_id = None
            user = request.myuser
            data = {
                'p_dir_id': request.POST.get('p_dir_id'),
                'label': request.POST.get('label'),
                'classify': request.POST.get('classify'),
                'note_premission': request.POST.get('note_premission')
            }
            files = request.FILES.getlist('myfiles')
            for f in files:
                data['content'] = f.read().decode('utf-8')
                data['note_name'] = f.name
                flag, task_id = Note().add_note(data, user)
                if not flag:
                    return JsonResponse(code[30003])
            task_progress(6, task_id)
            print('导入笔记进度完成')
            return JsonResponse(code[200])
        except Exception as e:
            print(e)
            return JsonResponse(code[30005])
    else:
        return JsonResponse(code[60001])


class UploadeImg(View):
    def post(self, request):
        try:
            img_files = request.FILES.get('images')
            try:
                suffix = img_files.name.split('.')[1]
                random_name = str(uuid.uuid4()) + '.' + suffix
            except Exception:
                random_name = str(uuid.uuid4()) + '.jpg'
            img_save_path = os.path.abspath('./media/images/') + '/' + random_name
            if not save_imgage(img_save_path, img_files):
                return JsonResponse(code[40019])
            server_addr = '/media/images/' + random_name
            res_data = code[200]
            res_data['img_addr'] = server_addr
            return JsonResponse(res_data)
        except Exception as e:
            print(e)
            return JsonResponse(code[30005])

    @class_login_check
    def get(self, request):
        img = request.GET.get('img')
        img_path = os.path.abspath('./media/images') + '/' + img
        os.remove(img_path)
        return JsonResponse(code[200])


def download_files(request):
    """
    文件下载
    :param request:
    :return:
    """
    if request.method == 'GET':
        try:
            file_id = request.GET.get('file_id')
            file_obj = File.objects.get(id=file_id)
            file_path = file_obj.file_path
            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename={}".format(quote(file_obj.file_name))
            return response
        except Exception as e:
            print(e)
            return JsonResponse(code[30005])
    else:
        return JsonResponse(code[60001])


def download_note(request):
    """
    笔记下载
    :param request:
    :return:
    """
    if request.method == 'GET':
        try:
            result = None
            note_id = request.GET.get('note_id')
            content_type = request.GET.get('type')
            token = request.GET.get('token')
            if not token:
                return JsonResponse(code[60002])
            users = token_return_user(token)
            if not users:
                return JsonResponse(code[10411])
            note_obj = Note.objects.get(id=note_id)
            print(note_obj.note_premission)
            print(users.user_permission)
            if note_obj.note_premission == 2 or users.user_permission == 1:
                # 公开
                print('公开')
                result = handle_type(content_type, note_obj)
                if not result:
                    return JsonResponse(code[40020])
            elif note_obj.note_premission == 1:
                # 内部公开
                task_obj = Task.objects.get(id=note_obj.task_id)
                print(json.loads(task_obj.particpant))
                print(users.id)
                if users.id in json.loads(task_obj.particpant) or users.id == note_obj.user_id:
                    result = handle_type(content_type, note_obj)
                    if not result:
                        return JsonResponse(code[40020])
                else:
                    return HttpResponse(json.dumps(code[40018], ensure_ascii=False), content_type='application/json')
            elif note_obj.note_premission == 0:
                # 仅自己
                if users.id == note_obj.user_id:
                    if content_type == 'pdf':
                        result = handle_type(content_type, note_obj)
                        if not result:
                            return JsonResponse(code[40020])
                else:
                    # return JsonResponse(code[40018])
                    return HttpResponse(json.dumps(code[40018], ensure_ascii=False), content_type='application/json')
            else:
                return HttpResponse(json.dumps(code[40018], ensure_ascii=False), content_type='application/json')
            return result
        except Exception as e:
            print(e)
            return JsonResponse(code[30006])
    else:
        return JsonResponse(code[60001])


def handle_type(content_type, note_obj):
    if content_type == 'pdf':
        res = pdf_md_transform(note_obj, 'pdf')
    else:
        res = pdf_md_transform(note_obj, 'md')
    return res


def pdf_md_transform(note_obj, transfoem_type):
    try:
        file_name = note_obj.note_name.split('.')[0]
        markdown2pdf_obj = MarkdownPdf()
        if transfoem_type == 'pdf':
            try:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment;  filename={}.pdf'.format(quote(file_name))
                output_filename = os.path.abspath('./media/pdf') + '/' + file_name + '.pdf'
                html_content = markdown2pdf_obj.md_to_html(note_obj.content)
                # 设置图片宽高
                html_content = html_content.replace('<img', '<img height="150" width="200"')
                print(html_content)
                markdown2pdf_obj.html_to_pdf(html_content, save_path=output_filename)
                with open(output_filename, 'rb') as fp:
                    response.write(fp.read())
                os.remove(output_filename)
                return response
            except Exception as e:
                print(e)
                return JsonResponse(code[60001])
        else:
            response = HttpResponse(content_type='application/md')
            html_content = markdown2pdf_obj.md_to_html(note_obj.content)
            text = markdown2pdf_obj.html_to_markdown(html_content)
            response['Content-Disposition'] = 'attachment; filename="{}.md"'.format(quote(file_name))
            response.write(text)
            return response
    except Exception as e:
        print(e)
        raise


def note_file_search(request):
    """ 笔记 文件搜索 """
    if request.method == 'GET':
        try:
            search = request.GET.get('search')
            keyword = request.GET.get('keyword')
            if not search:
                return JsonResponse(code[40013])
            page = request.GET.get('page')
            max_count = request.GET.get('max_count')
            if keyword == 'note':
                flag = request.GET.get('flag')
                data, total_page = Note().note_search(search, page, max_count, flag)
            elif keyword == 'file':
                data, total_page = File().file_search(search, page, max_count)
            else:
                return JsonResponse(code[60002])
            res_data = code[200]
            res_data['data'] = data
            res_data['total'] = total_page
            return JsonResponse(res_data)
        except Exception as e:
            err_info = code[60003]
            err_info['info'] = str(e)
            return JsonResponse(err_info)
    else:
        return JsonResponse(code[60001])


def knowledge_primary_page(request):
    get_task = int(request.GET.get('get_task'))
    search_word = request.GET.get('search_word')
    if get_task:
        result = Task().get_all_task()
        res_data = code[200]
        res_data['data'] = result
        return JsonResponse(res_data)

    elif not get_task and not search_word:
        task_id = request.GET.get('task_id')
        page = request.GET.get('page')
        max_count = request.GET.get('max_count')
        # 获取当前任务下笔记
        result, total = Note().know_note_info(task_id, page, max_count)
        res_data = code[200]
        res_data['data'] = result
        res_data['total'] = total
        return JsonResponse(res_data)

    elif search_word:
        # 搜索
        page = request.GET.get('page')
        max_count = request.GET.get('max_count')
        try:
            data_list, total_count = Task().search_task_all_note(
                page, max_count, search_word)
            res_data = code[200]
            res_data['data'] = data_list
            res_data['total'] = total_count
        except Exception as e:
            err_info = code[60003]
            err_info['info'] = str(e)
            return JsonResponse(err_info)
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


class ModifyQueryLabel(View):
    def get(self, request):
        result = Label().get_all_label()
        res_data = code[200]
        res_data['data'] = result
        return JsonResponse(res_data)

    def post(self, request):
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        label_name = data.get('label_name')
        label_id = data.get('label_id')
        if not Label().modify_label(label_id, label_name):
            return JsonResponse(code[40016])
        return JsonResponse(code[200])


class AddDelLabel(View):
    def post(self, request):
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        label_name = data.get('label_name')
        try:
            Label.objects.get(label_name=label_name)
            return JsonResponse(code[40014])
        except Exception as e:
            if not Label().add_label(label_name):
                return JsonResponse(code[40015])
        return JsonResponse(code[200])

    def get(self, request):
        label_id = int(request.GET.get('label_id'))
        Label.objects.filter(id=label_id).delete()
        return JsonResponse(code[200])


def know_note_details(request):
    if request.method == "GET":
        note_id = request.GET.get('note_id')
        data_dic = Note().query_note_info(note_id)
        res_data = code[200]
        res_data['data'] = data_dic.get('data', '')
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])
