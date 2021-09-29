# -*- coding: utf-8 -*-
import base64

from django.db import transaction
from django.http import JsonResponse

from Workplatform import settings
from Lanjian.user.models import UserInfo
from util.response_code import code
from util.util import judge_data_complate


def modify_user_info(request):
    """
    �û���ҳ��Ϣ����
    """
    if request.method == 'POST':
        body_data = request.body
        data = judge_data_complate(body_data)
        if not data:
            return JsonResponse(code[10001])
        name = data.get('username')
        permission = data.get('permission')
        engine = data.get('engine')
        api_key = data.get('api_key')
        user_id = data.get('user_id')
        avatar_data = data.get('avatar_data').split(',')
        img_data = base64.b64decode(avatar_data[1])
        img_name = name + settings.IMG_END
        # �ļ�����·��
        file_path = settings.MEDIA_ROOT + '/' + img_name
        net_path = settings.MEDIA_ADDR + '/' + img_name
        print(file_path)
        flag = False
        try:
            if upload_img_save(img_data, file_path):
                flag = True
        except Exception as e:
            print(e)
        try:
            user = UserInfo.objects.get(id=user_id)
            if user:
                return JsonResponse(code[10002])
            with transaction.atomic():
                user.user_permission = permission
                user.engine_type = engine
                user.api_key = api_key
                user.avatar = net_path
                user.save()
        except Exception:
            return JsonResponse(code[10403])
        if not flag:
            user.avatar = settings.DEFAULT_AVATAR
            return JsonResponse(code[10404])
        return JsonResponse(code[200])

from django.db import models
class Task(models.Model):
    title = models.CharField(max_length=1000, verbose_name='��������')
    description = models.TextField(verbose_name='��������', default='')
    particpant = models.CharField(max_length=200, verbose_name='���������Ա')
    end_time = models.CharField(max_length=20, null=True, verbose_name='�������ʱ��')
    start_time = models.CharField(max_length=20, verbose_name='����ʼʱ��')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='����ʱ��')
    update_time = models.DateTimeField(auto_now=True, verbose_name='����ʱ��')

    attack_source = models.BooleanField(default=False, verbose_name='���ع���Դ')
    collect_info = models.BooleanField(default=False, verbose_name='�ռ�����Ŀ����Ϣ')
    exploit_info = models.BooleanField(default=False, verbose_name='�ھ�©����Ϣ')
    get_target_premission = models.BooleanField(default=False, verbose_name='��ȡĿ�����Ȩ��')
    hide_attack = models.BooleanField(default=False, verbose_name='���ع�����Ϊ')
    start_attack = models.BooleanField(default=False, verbose_name='ʵʩ����')
    close_back_door = models.BooleanField(default=False, verbose_name='�رպ���')
    clear_attack_trace = models.BooleanField(default=False, verbose_name='��������ۼ�')

    host_num = models.IntegerField(verbose_name='��������', default=0)
    bug_num = models.IntegerField(verbose_name='©������', default=0)
    port_num = models.IntegerField(verbose_name='�˿�����', default=0)
    license_num = models.IntegerField(verbose_name='ƾ֤����', default=0)

    user = models.ForeignKey(UserInfo, verbose_name='�û�')