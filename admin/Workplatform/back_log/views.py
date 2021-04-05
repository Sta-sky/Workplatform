
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from taskmanage.models import BackNote, FileLog, NoteLog
from util.response_code import code


def query_all_backup_data(request):
    if request.method == 'GET':
        try:
            note_id = request.GET.get('note_id')
            data_dic = BackNote().query_all_backup_data(note_id)
            if not data_dic:
                return JsonResponse(code[40008])
            res_data = code[200]
            res_data['data'] = data_dic['data']
        except Exception:
            return JsonResponse(code[40005])
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


def return_backup_data(request):
    if request.method == 'GET':
        try:
            note_id = int(request.GET.get('note_id'))
            back_time = request.GET.get('back_time')
            flag = request.GET.get('flag')
            result = BackNote().return_back_time_data(note_id, back_time, flag)
            res_data = code[200]
            res_data['data'] = result
        except Exception:
            return JsonResponse(code[40005])
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])


def query_file_note_log(request):
    if request.method == 'GET':
        try:
            key_word = request.GET.get('key_word')
            task_id = request.GET.get('task_id')
            if key_word == 'file':
                result = FileLog().get_task_file_log(task_id)
            else:
                result = NoteLog().get_task_note_log(task_id)
            res_data = code[200]
            res_data['data'] = result
        except Exception as e:
            print(e)
            return JsonResponse(code[40017])
        return JsonResponse(res_data)
    else:
        return JsonResponse(code[60001])
