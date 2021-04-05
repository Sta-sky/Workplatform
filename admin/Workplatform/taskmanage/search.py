# -*- coding: utf-8 -*-
import json

import html2text
from django.db.models import Q
from django.http import JsonResponse

from adminq.models import TaskVulnerability, Host
from mind.models import MindNode, MindMap
from user.models import UserInfo
from util.logging_checked import def_login_check
from util.response_code import code
from util.util import get_page_info_list, get_total_page, handle_search_content
from taskmanage.models import Task, Note, File, Tool


@def_login_check
def all_search(request):
    try:
        keyword = request.GET.get('keyword')
        search_flag = request.GET.get('search_flag')
        max_count = int(request.GET.get('max_count'))
        page = int(request.GET.get('page'))
        myuser = request.myuser
        if not keyword:
            return JsonResponse(code[40013])
        if search_flag == 'note':
            my_filter = Q()
            my_filter = my_filter | Q(Q(note_name__icontains=keyword) | Q(content__icontains=keyword))
            note_obj = Note.objects.filter(Q(my_filter & ~Q(note_premission=0)) | my_filter & Q(user_id=myuser.id))
            if myuser.user_permission == 1:
                list_data, total_page = handle_note_search_info(note_obj, myuser, keyword, max_count, page)
            else:
                list_data, total_page = handle_note_search_info(note_obj, myuser, keyword, max_count, page)
        elif search_flag == 'file':
            file_obj = File.objects.filter(file_name__icontains=keyword)
            list_data, total_page = handle_file_search_info(file_obj, myuser, max_count, page)

        elif search_flag == 'host':
            host_obj = Host.objects.filter(Q(name__icontains=keyword) | Q(ip__icontains=keyword))
            list_data, total_page = handle_host_search_info(host_obj, myuser, max_count, page)

        elif search_flag == 'knowledge':
            note_obj = Note.objects.filter(Q(note_premission=2) & Q(note_name__icontains=keyword))
            list_data, total_page = handle_knowledge_search_info(note_obj, max_count, page, keyword)

        elif search_flag == 'mind':
            mind_obj = MindNode.objects.filter(Q(name__icontains=keyword) | Q(note__icontains=keyword))
            page_info_list = get_page_info_list(mind_obj, max_count, page)
            total_page = get_total_page(mind_obj, max_count)
            list_data = handle_mind_search_info(page_info_list)
        elif search_flag == 'loop':
            loop_obj = TaskVulnerability.objects.filter(name__icontains=keyword)
            page_info_list = get_page_info_list(loop_obj, max_count, page)
            total_page = get_total_page(loop_obj, max_count)
            list_data = handle_loop_search_info(page_info_list)
        else:
            return JsonResponse(code[60002])
        res_data = code[200]
        res_data['data'] = list_data
        res_data['total'] = total_page
        return JsonResponse(res_data)
    except Exception as e:
        print(e)


def handle_note_search_info(note_obj, myuser, keyword, max_count, page):
    data_lsit = []
    if not note_obj:
        return data_lsit, 0
    start_num, end_num = handle_pagetor(max_count, page)
    for info in note_obj:
        task = Task.objects.filter(id=info.task_id)[0]
        if myuser.user_permission != 1:
            # 普通用户既不是任务成员，也不是创建者
            if myuser.id not in json.loads(task.particpant) and myuser.id != info.user_id:
                continue
        task_user = UserInfo.objects.filter(id=task.user_id)[0]
        note_user = UserInfo.objects.filter(id=info.user_id)[0]
        pid_dir = Tool().find_pid(info.file_dir_id, info.note_name, 'note')
        content = handle_search_content(keyword, html2text.html2text(info.content))
        init_action = 'content'
        if not content:
            init_action = 'name'
            content = info.content[:50]
        data_dic = {
            'task_id': task.id,
            'task_name': task.title,
            'task_user': task_user.name,
            'note_id': info.id,
            'note_name': info.note_name,
            'note_path': pid_dir,
            'note_p_dir': info.file_dir_id,
            'note_contetn': content,
            'note_user': note_user.name,
            'is_name_content': init_action
        }
        data_lsit.append(data_dic)
    total_page = len(data_lsit)
    return data_lsit[start_num:end_num], total_page


def handle_file_search_info(file_obj, myuser, max_count, page):
    data_lsit = []
    if not file_obj:
        return data_lsit, 0
    start_num, end_num = handle_pagetor(max_count, page)
    for info in file_obj:
        task = Task.objects.filter(id=info.task_id)[0]
        if myuser.id != 1 and myuser.id not in json.loads(task.particpant) and myuser.id != info.user_id:
            continue
        task_user = UserInfo.objects.filter(id=task.user_id)[0]
        file_user = UserInfo.objects.filter(id=info.user_id)[0]
        pid_dir = Tool().find_pid(info.file_dir_id, info.file_name, 'file')
        data_dic = {
            'task_id': task.id,
            'task_name': task.title,
            'task_user': task_user.name,
            'file_id': info.id,
            'file_name': info.file_name,
            'file_path': pid_dir,
            'file_p_dir': info.file_dir_id,
            'file_description': info.description,
            'file_user': file_user.name,
        }
        data_lsit.append(data_dic)
    total_page = len(data_lsit)
    return data_lsit[start_num:end_num], total_page


def handle_host_search_info(host_obj, myuser, max_count, page):
    data_list = []
    if not host_obj:
        return data_list, 0
    start_num, end_num = handle_pagetor(max_count, page)
    for info in host_obj:
        host_obj = Host.objects.filter(id=info.id)[0]
        task_obj = Task.objects.filter(id=host_obj.task_id)[0]
        if myuser.id != 1 and myuser.id not in json.loads(task_obj.particpant):
            continue
        host_user_obj = UserInfo.objects.filter(id=host_obj.user_id)[0]
        task_user_obj = UserInfo.objects.filter(id=task_obj.user_id)[0]
        data_dic = {
            'task_id': task_obj.id,
            'task_name': task_obj.title,
            'task_user': task_user_obj.name,
            'host_id': host_obj.id,
            'host_name': host_obj.name,
            'host_ip': host_obj.ip,
            'create_user': host_user_obj.name
        }
        data_list.append(data_dic)
    total_page = len(data_list)
    return data_list[start_num:end_num], total_page


def handle_knowledge_search_info(knowledge_obj, max_count, page, keyword):
    data_lsit = []
    if not knowledge_obj:
        return data_lsit, 0
    start_num, end_num = handle_pagetor(max_count, page)
    for info in knowledge_obj:
        task = Task.objects.filter(id=info.task_id)[0]
        task_user = UserInfo.objects.filter(id=task.user_id)[0]
        note_user = UserInfo.objects.filter(id=info.user_id)[0]
        content = handle_search_content(keyword, html2text.html2text(info.content))
        init_action = 'content'
        if not content:
            init_action = 'name'
            content = info.content[:50]
        data_dic = {
            'task_id': task.id,
            'task_name': task.title,
            'task_user': task_user.name,
            'note_id': info.id,
            'note_name': info.note_name,
            'note_p_dir': info.file_dir_id,
            'note_contetn': content,
            'note_user': note_user.name,
            'is_name_content': init_action
        }
        data_lsit.append(data_dic)
    total_page = len(data_lsit)
    return data_lsit[start_num:end_num], total_page


def handle_mind_search_info(page_info_list):
    data_list = []
    if not page_info_list:
        return data_list
    for info in page_info_list:
        node_obj = MindNode.objects.filter(id=info.id)[0]
        mind_obj = MindMap.objects.filter(id=node_obj.mind_id)[0]
        task_obj = Task.objects.filter(id=mind_obj.task_id)[0]
        mind_user_obj = UserInfo.objects.filter(id=mind_obj.user_id)[0]
        task_user_obj = UserInfo.objects.filter(id=task_obj.user_id)[0]
        note = node_obj.note
        if note:
            note = note[:50]
        data_dic = {
            'task_id': task_obj.id,
            'task_name': task_obj.title,
            'task_user': task_user_obj.name,
            'node_id': node_obj.id,
            'node_name': node_obj.name,
            'node_note': note,
            'mind_map_title': mind_obj.title,
            'mind_map_id': mind_obj.id,
            'mind_map_user': mind_user_obj.name
        }
        data_list.append(data_dic)
    return data_list


def handle_loop_search_info(page_info_list):
    data_list = []
    if not page_info_list:
        return data_list
    for info in page_info_list:
        loop_obj = TaskVulnerability.objects.filter(id=info.id)[0]
        task_obj = Task.objects.filter(id=loop_obj.task_id)[0]
        host_obj = Host.objects.filter(id=info.host_id)[0]
        loop_user_obj = UserInfo.objects.filter(id=loop_obj.user_id)[0]
        task_user_obj = UserInfo.objects.filter(id=task_obj.user_id)[0]
        data_dic = {
            'task_id': task_obj.id,
            'task_name': task_obj.title,
            'task_user': task_user_obj.name,
            'loop_id': loop_obj.id,
            'loop_name': loop_obj.name,
            'loop_description': loop_obj.describe[:50],
            'loop_host': host_obj.name,
            'risk_rank': loop_obj.level,
            'create_user': loop_user_obj.name
        }
        data_list.append(data_dic)
    return data_list


def handle_pagetor(max_count, page):
    start_num = 0
    end_num = max_count
    if page > 1:
        start_num = page * max_count - max_count
        end_num = page * max_count
    return start_num, end_num
