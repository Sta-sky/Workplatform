# -*- coding: utf-8 -*-
import json

import html2text
from django.db import models, transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.timezone import now

from user.models import UserInfo
from util.redis_connect import Redis
from util.util import handle_search_content, get_total_page, get_page_info_list


# 任务表
class Task(models.Model):
    title = models.CharField(max_length=1000, verbose_name='任务名称')
    description = models.TextField(verbose_name='任务描述', default='')
    particpant = models.CharField(max_length=200, verbose_name='任务参与人员')
    end_time = models.DateTimeField(max_length=20, null=True, verbose_name='任务结束时间')
    start_time = models.DateTimeField(max_length=20, verbose_name='任务开始时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    task_process = models.CharField(max_length=50, default=0, verbose_name='任务进度')
    user = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)

    class Meta:
        db_table = 'task'

        verbose_name_plural = '任务表'

    @classmethod
    def create_task(cls, data, user):
        """  创建任务 """
        title = data.get('title')
        description = data.get('description')
        participant = json.dumps(data.get('participant'))
        end_time = data.get('end_time')
        start_time = data.get('start_time')
        tasks = Task.objects.filter(title=title)
        if tasks.exists():
            return False
        try:
            with transaction.atomic():
                task = Task.objects.create(
                    title=title,
                    description=description,
                    particpant=participant,
                    start_time=start_time,
                    end_time=end_time,
                    user_id=user.id
                )
            return task
        except Exception as e:
            print(e)
            return False

    @classmethod
    def delete_task(cls, task_id):
        """删除任务  包括任务下所有笔记、目录、文件、缓存 """
        try:
            task = Task.objects.get(id=task_id)
            if task.user.task_count > 0:
                task.user.task_count -= 1
            task.user.save()
            Task.objects.filter(id=task_id).delete()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def modify_task(cls, data):
        """ 修改任务 """
        task_id = data.get('task_id')
        title = data.get('title')
        description = data.get('description')
        participant = json.dumps(data.get('participant'))
        end_time = data.get('end_time')
        start_time = data.get('start_time')
        try:
            task = Task.objects.get(id=task_id)
            task.title = title
            task.description = description
            task.particpant = participant
            task.end_time = end_time
            task.start_time = start_time
            task.save()
            print('保存完成')
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def query_all_task(cls, page, max_count, search_word, user):
        """
        任务展示页数据查询
        """
        try:
            if not search_word:
                if user.user_permission == 1:
                    # 管理员
                    task_permission = 1
                    task_obj = Task.objects.all().order_by('create_time')
                    pagetor = Paginator(task_obj, int(max_count))
                    total_page = pagetor.count
                    page_list_info = pagetor.page(int(page))
                else:
                    # 参与者、 创建者
                    page_list_info = []
                    task_permission = 0
                    task_obj = Task.objects.all().order_by('create_time')
                    for info in task_obj:
                        if user.id in json.loads(info.particpant) or info.user_id == user.id:
                            page_list_info.append(info)
                    total_page = len(page_list_info)
                result = Task().handle_admin_info(page_list_info)
                return result, total_page, task_permission
            else:
                # 搜索
                if user.user_permission == 1:
                    task_permission = 1
                    task_obj = Task.objects.filter(title__icontains=search_word).order_by('create_time')
                    pagetor = Paginator(task_obj, int(max_count))
                    total_page = pagetor.count
                    page_list_info = pagetor.page(int(page))
                else:
                    task_permission = 0
                    page_list_info = []
                    task_obj = Task.objects.filter(title__icontains=search_word).order_by('create_time')
                    for search_info in task_obj:
                        if user.id in json.loads(search_info.particpant) or search_info.user_id == user.id:
                            page_list_info.append(search_info)
                    total_page = len(page_list_info)
                result = Task().handle_admin_info(page_list_info)
                return result, total_page, task_permission
        except Exception as e:
            print(e)
            return None, None, None

    @classmethod
    def handle_admin_info(cls, page_list_info):
        data_list = []
        for info in page_list_info:
            user_obj = UserInfo.objects.get(id=info.user_id)
            data_dic = {
                'particpant': json.loads(info.particpant),
                'title': info.title,
                'start_time': info.start_time.strftime('%Y-%m-%d'),
                'end_time': info.end_time.strftime('%Y-%m-%d'),
                'task_process': Task().handle_process(info),
                'task_id': info.id,
                'user': user_obj.name,
                'user_id': info.user_id,
                'description': info.description
            }
            data_list.append(data_dic)
        return data_list

    @classmethod
    def handle_process(cls, info_obj):
        process_time = now() - info_obj.start_time
        task_time = info_obj.end_time - info_obj.start_time
        process = process_time.days / task_time.days
        if process > 1:
            process = 1
        if process < 0:
            process = 0
        return f'{process * 100:.0f}'

    @classmethod
    def query_task_detail(cls, task_id):
        """查询对应任务的详细信息"""
        try:
            task = Task.objects.get(id=task_id)
            task_detail_dic = {
                'title': task.title,
                'description': task.description,
                'particpant': json.loads(task.particpant),
                'start_time': task.start_time,
                'end_time': task.end_time,
                'task_process': task.task_process
            }
            return True, task_detail_dic
        except Exception:
            return False, {}

    @classmethod
    def get_all_task(cls):
        task = Task.objects.values_list('title', 'id')
        task_list = []
        for info in task:
            task_dic = {
                'title': info[0],
                'id': info[1]
            }
            task_list.append(task_dic)
        return task_list

    @classmethod
    def search_task_all_note(
            cls, page, max_count, search_word):
        total_count = 0
        try:
            note = Note.objects.filter(note_name__icontains=search_word).order_by('update_time')
            pagetor = Paginator(note, max_count)
            total_count += pagetor.count
            page_info_list = pagetor.page(page)
            data_list = []
            for info in page_info_list:
                data_dic = {
                    'note_name': info.note_name,
                    'label': info.label.label_name,
                    'classify': info.classify,
                    'create_user': info.user.name,
                    'create_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                data_list.append(data_dic)
            return data_list, total_count
        except Exception as e:
            print(e)
            return [], None

    @classmethod
    def get_title(cls, task_id):
        try:
            task = Task.objects.get(id=task_id)
            return task.title
        except Exception as e:
            print(e)
            return False


# 笔记标签表
class Label(models.Model):
    label_name = models.CharField(max_length=100, verbose_name='笔记类别表')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')

    class Meta:
        db_table = 'classes'
        verbose_name_plural = '笔记类别表'

    @classmethod
    def get_all_label(cls):
        try:
            user_list = []
            user = Label.objects.all()
            for info in user:
                user_dic = {
                    'id': info.id,
                    'name': info.label_name
                }
                user_list.append(user_dic)
            return user_list
        except Exception as e:
            return []

    @classmethod
    def add_label(cls, label_name):
        try:
            Label.objects.create(label_name=label_name)
            return True
        except Exception as e:
            return False

    @classmethod
    def modify_label(cls, label_id, label_name):
        try:
            label_obj = Label.objects.get(id=label_id)
            label_obj.label_name = label_name
            label_obj.save()
            return True
        except Exception as e:
            return False


# 笔记文件目录表
class NoteDir(models.Model):
    file_name = models.CharField(max_length=1000, verbose_name='文件目录')
    sub_dir = models.CharField(max_length=500, verbose_name='文件子目录id', null=True, default='')
    pid = models.CharField(max_length=50, verbose_name='父目录id')
    is_primary_dir = models.BooleanField(default=False, verbose_name='是否为根目录')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    task = models.ForeignKey(Task, verbose_name='任务', on_delete=models.CASCADE)

    class Meta:
        db_table = 'note_dir'
        verbose_name_plural = '文件目录表'

    @classmethod
    def create_dir(cls, data):
        """ 创建文件目录，"""
        pid = data.get('pid')
        primary = data.get('primary')
        file_name = data.get('filename')
        task_id = data.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
            if primary == 1:
                filter_res = NoteDir.objects.filter(file_name=file_name, task_id=task_id)
                if filter_res.exists():
                    return False
                NoteDir.objects.create(
                    file_name=file_name, task_id=task.id, is_primary_dir=True)
            else:
                dirs = NoteDir.objects.get(id=pid)
                p_dir = NoteDir.objects.create(file_name=file_name, task_id=task.id, pid=pid)
                if dirs.sub_dir:
                    sub_dir_id = str(dirs.sub_dir) + '_' + str(p_dir.id)
                else:
                    sub_dir_id = str(p_dir.id)
                dirs.sub_dir = sub_dir_id
                dirs.save()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def modify_dir_name(cls, data):
        """ 修改目录名称 """
        dir_id = data.get('dir_id')
        dir_name = data.get('dir_name')
        try:
            dir_obj = NoteDir.objects.get(id=dir_id)
            dir_obj.file_name = dir_name
            dir_obj.save()
        except Exception as e:
            print(e)
            raise


# 笔记表
class Note(models.Model):
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

    class Meta:
        db_table = 'note'

    @classmethod
    def query_file_dir(cls, task_id, page, max_count, is_primary=True, dir_id=None):
        """ 查询文件 目录树 """
        Task.objects.get(id=task_id)
        try:
            print(is_primary)
            if is_primary:
                notes = NoteDir.objects.filter(task_id=task_id, is_primary_dir=is_primary)
            else:
                notes = NoteDir.objects.get(id=dir_id, task_id=task_id)
            if is_primary:
                data_list = []
                for info in notes:
                    data_dic_sub = {
                        'dir_name': info.file_name,
                        'id': info.id
                    }
                    data_list.append(data_dic_sub)
                note_info, total_page = Note().task_dir_get_all_note(task_id, max_count, page)
                data_dic = {
                    'dir_name': 'primary',
                    'id': None,
                    'sub_dir': data_list,
                    'note_info': note_info,
                    'total': total_page
                }
            else:
                file_sub_dir = Note().handle_sub_dir(notes.sub_dir)
                note_info, total_page = Note().dir_id_query_note(dir_id, max_count, page)
                data_dic = {
                    'dir_name': notes.file_name,
                    'id': notes.id,
                    'sub_dir': file_sub_dir,
                    'note_info': note_info,
                    'total': total_page
                }
            return data_dic
        except Exception as e:
            print(e)
            raise

    @classmethod
    def add_note(cls, data, user):
        """
        添加笔记
        """
        try:
            p_dir_id = data.get('p_dir_id')
            note_name = data.get('note_name')
            content = data.get('content')
            label_id = data.get('label')
            if not label_id:
                label_id = 1
            classify = data.get('classify')
            note_premission = data.get('note_premission')
            p_dir = NoteDir.objects.get(id=p_dir_id)
            task_id = p_dir.task.id
            label = Label.objects.get(id=label_id)
            Note.objects.create(
                note_name=note_name,
                content=content,
                note_premission=note_premission,
                classify=classify,
                file_dir_id=p_dir_id,
                label=label,
                user=user,
                task_id=task_id
            )
            NoteLog().write_note_action_log(action=1, note_name=note_name, user_id=user.id, task_id=task_id)
            return True, task_id
        except Exception as e:
            print(e)
            return False, None

    @classmethod
    def modify_note(cls, data, user):
        redis_obj = Redis('note')
        note_id = data.get('note_id')
        note_name = data.get('note_name')
        content = data.get('content')
        note_premission = data.get('note_premission')
        label = data.get('label')
        classify = data.get('classify')
        label_obj = Label.objects.get(label_name=label)
        try:
            note = Note.objects.get(id=note_id)
            note.note_name = note_name
            note.content = content
            note.note_premission = note_premission
            note.label = label_obj
            note.classify = classify
            note.save()
            # 备份
            update_time = note.update_time
            BackNote().create_back(content, update_time, note_id, user)
            task_id = note.file_dir.task_id
            NoteLog().write_note_action_log(action=2, note_name=note_name, user_id=user.id, task_id=task_id)
            redis_obj.delete_lock(str(note_id))
            return True
        except Exception as e:
            redis_obj.delete_lock(str(note_id))
            return False

    @classmethod
    def query_note_info(cls, note_id):
        """note_id  笔记id查询单个笔记详细信息"""
        try:
            back_info = BackNote().query_all_backup_data(int(note_id))
            note = Note.objects.get(id=note_id)
            data = {
                'id': note.id,
                'back_info': back_info,
                'user': note.user.name,
                'content': note.content,
                'classify': note.classify,
                'note_name': note.note_name,
                'label': note.label.label_name,
                'belong_to_dir': note.file_dir.file_name,
                'note_premission': note.note_premission,
                'create_time': note.create_time.strftime('%Y-%m-%d %H:%M:%S'),

            }
            data_dic = {
                'data': data
            }
            return data_dic
        except Exception as e:
            print(e)
            return {}

    @classmethod
    def dir_id_query_note(cls, dir_id, max_count, page):
        """目录id 查询目录下所有笔记 """
        try:
            note = Note.objects.filter(file_dir=dir_id).order_by('-update_time')
            total_page = get_total_page(note, max_count)
            page_info_list = get_page_info_list(note, max_count, page)
            info_list = Note().handle_queryset_info(page_info_list)
            return info_list, total_page
        except Exception:
            return [], None

    @classmethod
    def task_dir_get_all_note(cls, task_id, max_count, page):
        """根据 任务id获取任务下所有笔记"""
        try:
            note_info = Note.objects.filter(task_id=task_id).order_by('-update_time')
            total_page = get_total_page(note_info, max_count)
            page_info_list = get_page_info_list(note_info, max_count, page)
            info_list = Note().handle_queryset_info(page_info_list)
            return info_list, total_page
        except Exception as e:
            print(e)
            return [], None

    @classmethod
    def note_search(cls, keyword, page, max_count, flag):
        flag_res = False
        try:
            if flag == 'content':
                note = Note.objects.filter(content__icontains=keyword)
            else:
                flag_res = True
                note = Note.objects.filter(note_name__icontains=keyword)
            total_page = get_total_page(note, max_count)
            current_page_info_list = get_page_info_list(note, max_count, page)
            note_list = []
            for info in current_page_info_list:
                if not flag_res:
                    content = handle_search_content(keyword, html2text.html2text(info.content))
                else:
                    content = html2text.html2text(info.content)[:50]
                note_dic = {
                    'note_name': info.note_name,
                    'note_id': info.id,
                    'content': content,
                    'note_premission': info.note_premission,
                    'classify': info.classify,
                    'label': info.label.label_name,
                    'file_dir': Tool().find_pid(info.file_dir_id, info.note_name, 'note')
                }
                note_list.append(note_dic)
            return note_list, total_page
        except Exception as e:
            print(e)
            return [], None

    @classmethod
    def handle_queryset_info(cls, queryset_obj):
        info_list = []
        for info in queryset_obj:
            info_dic = {
                'note_name': info.note_name,
                'note_id': info.id,
                'content': html2text.html2text(info.content),
                'note_premission': info.note_premission,
                'label': info.label.label_name,
                'classify': info.classify
            }

            info_list.append(info_dic)
        return info_list

    @classmethod
    def handle_sub_dir(cls, sub_dir):
        """
            处理子目录
        """
        if len(sub_dir.split('_')) < 1 or not sub_dir:
            return []
        else:
            file_info_list = []
            sub_res = sub_dir.split('_')
            for _id in sub_res:
                file = NoteDir.objects.filter(id=int(_id))[0]
                file_info_dic = {
                    'dir_name': file.file_name,
                    'id': file.id
                }
                file_info_list.append(file_info_dic)
        return file_info_list

    @classmethod
    def know_note_info(cls, task_id, page, max_count):
        """知识库中 对应任务中所有笔记信息"""
        data_list = []
        note = Note.objects.filter(task_id=task_id, note_premission=2).order_by('-update_time')
        total_count = get_total_page(note, max_count)
        page_info_list = get_page_info_list(note, max_count, page)
        for info in page_info_list:
            data_dic = {
                'id': info.id,
                'classify': info.classify,
                'note_name': info.note_name,
                'create_user': info.user.name,
                'label': info.label.label_name,
                'create_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            data_list.append(data_dic)
        return data_list, total_count


# 备份笔记表
class BackNote(models.Model):
    content = models.TextField(verbose_name='备份内容')
    back_time = models.CharField(max_length=100, verbose_name='备份时间')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    note = models.ForeignKey(Note, verbose_name='备份数据对应的笔记', on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, verbose_name='修改用户', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='关联任务', on_delete=models.CASCADE)

    class Meta:
        db_table = 'backupnote'

    @classmethod
    def create_back(cls, content, update_time, note_id, user):
        """创建备份数据"""
        try:
            note = Note.objects.get(id=note_id)
            date = str(update_time).split('.')[0] + '.' + str(update_time).split('.')[1][0:2]
            BackNote.objects.create(
                content=content,
                back_time=date,
                note=note,
                user=user,
                task_id=note.task_id
            )
        except Exception as e:
            raise

    @classmethod
    def query_all_backup_data(cls, note_id):
        """note_id对应笔记的所有备份数据查询"""
        try:
            back_note = BackNote.objects.filter(note_id=note_id).order_by('-create_time')
            back_data_list = []
            user = Note.objects.get(id=note_id)
            username = user.file_dir.task.user.name
            for info in back_note:
                back_data_dic = {
                   'back_time': info.back_time,
                   'back_user': username
                }
                back_data_list.append(back_data_dic)
            return back_data_list
        except Exception as e:
            print(e)
            return []

    @classmethod
    def return_back_time_data(cls, note_id, backup_time, flag):
        """备份数据回退"""
        try:
            back = BackNote.objects.filter(back_time=backup_time, note_id=note_id)[0]
            content = back.content
            back_time = back.back_time
            if flag == '1':
                pass
            elif flag == '2':
                note_obj = Note.objects.get(id=note_id)
                note_obj.content = content
                note_obj.save()
            else:
                return {}
            data_dic = {
                'content': content,
                'back_time': back_time
            }
            return data_dic
        except Exception as e:
            print(e)
            return {}

    @classmethod
    def note_id_delete(cls, note_id):
        """
        当任务删除时  删除任务下，所有关联的文件夹
        """
        try:
            BackNote.objects.filter(note_id=note_id).delete()
        except Exception as e:
            print(e)
            raise


# 文件目录表
class FileDir(models.Model):
    dir_name = models.CharField(max_length=100, verbose_name='目录名称')
    sub_dir = models.CharField(max_length=500, verbose_name='子目录id', null=True, default='')
    pid = models.CharField(max_length=50, verbose_name='父目录id')
    is_primary_dir = models.BooleanField(default=False, verbose_name='是否为根目录')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    task = models.ForeignKey(Task, verbose_name='任务', on_delete=models.CASCADE)

    class Meta:
        db_table = 'file_dir'
        verbose_name_plural = '文件目录表'

    @classmethod
    def create_dir(cls, data):
        """
        创建文件目录，
        """
        pid = data.get('pid')
        primary = data.get('primary')
        file_name = data.get('filename')
        task_id = int(data.get('task_id'))
        try:
            task = Task.objects.get(id=task_id)
            if primary == 1:
                filter_res = FileDir.objects.filter(dir_name=file_name, task_id=task_id)
                if filter_res.exists():
                    return False
                FileDir.objects.create(
                    dir_name=file_name, task_id=task.id, is_primary_dir=True)
            else:
                pid = int(pid)
                dirs = FileDir.objects.get(id=pid)
                p_dir = FileDir.objects.create(dir_name=file_name, task_id=task.id, pid=pid)
                if dirs.sub_dir:
                    sub_dir_id = str(dirs.sub_dir) + '_' + str(p_dir.id)
                else:
                    sub_dir_id = str(p_dir.id)
                dirs.sub_dir = sub_dir_id
                dirs.save()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def modify_dir_name(cls, data):
        """
        修改目录名称
        """
        dir_id = data.get('dir_id')
        dir_name = data.get('dir_name')
        try:
            dir_obj = FileDir.objects.get(id=dir_id)
            dir_obj.dir_name = dir_name
            dir_obj.save()
        except Exception as e:
            print(e)
            raise


# 文件表
class File(models.Model):
    file_name = models.CharField(max_length=100, verbose_name='文件名称')
    file_path = models.CharField(max_length=100, verbose_name='文件内容')
    description = models.CharField(max_length=1000, verbose_name='文件描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    file_dir = models.ForeignKey(FileDir, verbose_name='所属文件目录', on_delete=models.CASCADE)
    box_check = models.CharField(max_length=100, null=True, verbose_name='沙箱检测')
    user = models.ForeignKey(UserInfo, verbose_name='创建用户', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='对应任务', on_delete=models.CASCADE)

    class Meta:
        db_table = 'file'

    @classmethod
    def query_file_dir(cls, task_id, page, max_count, is_primary=True, dir_id=None):
        """
        查询文件 目录树
        """
        try:
            if is_primary:
                files = FileDir.objects.filter(task_id=task_id, is_primary_dir=is_primary)
            else:
                # 子目录跟父目录  都要查询  所有不能加 is_primary参数，
                files = FileDir.objects.get(id=dir_id, task_id=task_id)
            if is_primary:
                data_list = []
                for info in files:
                    data_dic_sub = {
                        'id': info.id,
                        'dir_name': info.dir_name
                    }
                    data_list.append(data_dic_sub)
                file_info, total_page = File().task_dir_get_all_file(task_id, max_count, page)
                data_dic = {
                    'id': None,
                    'dir_name': 'primary',
                    'sub_dir': data_list,
                    'file_info': file_info,
                    'total': total_page
                }
            else:
                file_info, total_page = File().dir_id_query_file(dir_id, max_count, page)
                file_sub_dir = File().handle_sub_dir(files.sub_dir)
                data_dic = {
                    'id': files.id,
                    'total': total_page,
                    'file_info': file_info,
                    'sub_dir': file_sub_dir,
                    'dir_name': files.dir_name
                }
            return data_dic
        except Exception as e:
            print(e)
            return {}

    @classmethod
    def dir_id_query_file(cls, dir_id, max_count, page):
        """
            查询文件
        :param dir_id:
        :return:
        """
        try:
            file_info = File.objects.filter(file_dir=dir_id)
            total = get_total_page(file_info, max_count)
            page_info_list = get_page_info_list(file_info, max_count, page)
            info_lists = File().handle_queryset_info(page_info_list)
            return info_lists, total
        except Exception:
            return [], None

    @classmethod
    def handle_queryset_info(cls, queryset_obj):
        info_list = []
        for info in queryset_obj:
            info_dic = {
                'file_id': info.id,
                'file_name': info.file_name,
                'description': info.description,
                'create_user': info.user.name,
                'create_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            info_list.append(info_dic)
        return info_list

    @classmethod
    def handle_sub_dir(cls, sub_dir):
        """
        处理子目录
        """
        if len(sub_dir.split('_')) < 1 or not sub_dir:
            return []
        else:
            file_info_list = []
            sub_res = sub_dir.split('_')
            for id_ in sub_res:
                file = FileDir.objects.filter(id=int(id_))[0]
                file_info_dic = {
                    'dir_name': file.dir_name,
                    'id': file.id
                }
                file_info_list.append(file_info_dic)
        return file_info_list

    @classmethod
    def add_file(cls, pid, description, file_name, save_path, user):
        """
        添加文件
        """
        try:
            p_dir = FileDir.objects.get(id=pid)
            task_id = p_dir.task_id
            File.objects.create(
                file_name=file_name,
                file_path=save_path,
                file_dir=p_dir,
                description=description,
                user=user,
                task_id=task_id
            )
            FileLog().write_file_action_log(action=1, user_id=user.id, file_name=file_name, task_id=task_id)
            return True, task_id
        except Exception as e:
            return False, None

    @classmethod
    def task_dir_get_all_file(cls, task_id, max_count, page):
        try:
            file_info = File.objects.filter(task_id=task_id)
            total = get_total_page(file_info, max_count)
            page_info_list = get_page_info_list(file_info, max_count, page)
            info_lists = File().handle_queryset_info(page_info_list)
            return info_lists, total
        except Exception as e:
            return [], None

    @classmethod
    def file_search(cls, search, page, max_count):
        file = File.objects.filter(file_name__icontains=search)
        total = get_total_page(file, max_count)
        page_info_list = get_page_info_list(file, max_count, page)
        info_list = []
        for info in page_info_list:
            file_path = Tool().find_pid(info.file_dir_id, info.file_name, 'file')
            info_dic = {
                'file_name': info.file_name,
                'file_id': info.id,
                'create_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'create_user': info.user.name,
                'box_check': info.box_check,
                'file_dir': file_path
            }
            info_list.append(info_dic)
        return info_list, total


class FileLog(models.Model):
    action = models.IntegerField(verbose_name='执行动作', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    file_name = models.CharField(max_length=200, verbose_name='文件名称')
    user_id = models.IntegerField(verbose_name='用户id')
    task = models.ForeignKey(Task, verbose_name='对应任务', on_delete=models.CASCADE)

    class Meta:
        db_table = 'file_log'

    @classmethod
    def write_file_action_log(cls, action, user_id, file_name, task_id):
        FileLog.objects.create(
            action=action,
            file_name=file_name,
            user_id=user_id,
            task_id=task_id
        )

    @classmethod
    def get_task_file_log(cls, task_id):
        try:
            action_data_list = []
            file = FileLog.objects.filter(task_id=task_id).order_by('-create_time')[:100]
            for info in file:
                user = UserInfo.objects.get(id=info.user_id)
                action_data_dic = {
                    'action': info.action,
                    'user_name': user.name,
                    'file_name': info.file_name,
                    'log_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                action_data_list.append(action_data_dic)
            print(action_data_list)
            return action_data_list
        except Exception as e:
            print('获取文件日志失败，原因为：', e)
            return []


class NoteLog(models.Model):
    action = models.IntegerField(verbose_name='执行动作', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    note_name = models.CharField(max_length=200, verbose_name='文件名称')
    user_id = models.IntegerField(verbose_name='用户id')
    task = models.ForeignKey(Task, verbose_name='任务', on_delete=models.CASCADE)

    class Meta:
        db_table = 'note_log'

    @classmethod
    def write_note_action_log(cls, action, note_name, user_id, task_id):
        """笔记操作日志写入"""
        try:
            NoteLog.objects.create(
                action=action,
                note_name=note_name,
                user_id=user_id,
                task_id=task_id
            )
        except Exception as e:
            print(e)
            raise

    @classmethod
    def get_task_note_log(cls, task_id):
        """根据任务id 获取任务下所有笔记操作的日志，按时间排序"""
        try:
            action_data_list = []
            note = NoteLog.objects.filter(task_id=task_id).order_by('-create_time')[:100]
            for info in note:
                user = UserInfo.objects.get(id=info.user_id)
                action_data_dic = {
                    'action': info.action,
                    'user_name': user.name,
                    'action_time': info.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'note_name': info.note_name
                }
                action_data_list.append(action_data_dic)
            return action_data_list
        except Exception as e:
            print('获取笔记日志失败，原因为：', e)
            return []


class Tool(object):
    @classmethod
    def find_pid(cls, dir_pid, name, flag):
        path_dir = '/' + str(name)
        if flag == 'note':
            while True:
                dir_obj = NoteDir.objects.get(id=dir_pid)
                key = '/' + str(dir_obj.file_name)
                path_dir = key + path_dir.ljust(0)
                dir_pid = dir_obj.pid
                if not dir_obj.pid:
                    break
            return path_dir
        elif flag == 'file':
            while True:
                dir_obj = FileDir.objects.get(id=dir_pid)
                key = '/' + str(dir_obj.dir_name)
                path_dir = key + path_dir.ljust(0)
                dir_pid = dir_obj.pid
                if not dir_obj.pid:
                    break
            return path_dir
        else:
            return False
