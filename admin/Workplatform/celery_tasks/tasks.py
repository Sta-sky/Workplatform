import os
import json
import time
import random
import shutil
import requests
from util.util import win_zip_tool
from celery_tasks.main import celery_app
from mind.models import OpenDir, MindNode
from webscanApp.utils import dirsearch_func
from celery.task import periodic_task
from celery.schedules import crontab
from Workplatform.settings import mysql_username, mysql_pwd, db
from adminq.models import BackupRecord
from Workplatform.settings import BASE_DIR


# 站点目录扫描
@celery_app.task
def dirsearch_task(site, report_name, config={}):
    report_path = dirsearch_func(site, report_name, config)
    if not report_path:
        return
    for _ in range(10):
        if not os.path.exists(report_path):
            time.sleep(5)
            continue
        else:
            with open(report_path, 'r', encoding='utf-8') as f:
                dir_obj = OpenDir()
                dir_obj.note = MindNode.objects.get(id=site)
                dir_obj.dir = f.read()
                dir_obj.save()
                print(f'节点:{site} 保存目录扫描结果完毕')


# 更新任务进度
@periodic_task(run_every=crontab())
def update_task_progress():
    print("1")


# 数据备份
@celery_app.task(name='backup')
def back_celery(back_id):
    # 获取备份记录
    win_flag = False
    if os.name == 'nt':
        win_flag = True
    back = BackupRecord.objects.filter(id=back_id).first()
    path = BASE_DIR + "/backups"
    meida_path = BASE_DIR + "/media"
    file = "backup" + str(time.time()).split(".")[0]
    back.progress = 10
    back.save()
    os.mkdir(path + "/" + file)
    file_path = path + "/" + file
    # 数据库移动
    sql_cmd = f"mysqldump -u{mysql_username} " \
              f"-p{mysql_pwd} {db} > {file_path}/db1.sql"
    os.system(sql_cmd)
    # 移动文件到目录下
    
    if win_flag:
        print(file_path)
        shutil.copytree(meida_path, file_path + '/media')
    else:
        cmd = "cp -r " + meida_path + " " + file_path
        os.system(cmd)
    back.progress = 50
    back.save()
    if win_flag:
        win_zip_tool(meida_path, file_path + '/' + file + '.zip')
    else:
        zip_cmd = "zip -r -m -P yth@!@#qzmp " + file + ".zip " + file
        os.system('cd backups && ' + zip_cmd)
    back.progress = 100
    back.status = 1
    back.backup_filepath = file_path + ".zip"
    back.save()
