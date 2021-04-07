import os
import time

from Workplatform.settings import mysql_username, mysql_pwd, db

from adminq.models import BackupRecord

from Workplatform.settings import BASE_DIR
from celery import task


@task(name="backup")
def backup(args):
    # 获取备份记录
    back = BackupRecord.objects.filter(id=args).first()
    path = BASE_DIR + "/backups"
    meida_path = BASE_DIR + "/media"
    file = "backup" + str(time.time()).split(".")[0]
    back.progress = 10
    back.save()
    os.mkdir(path + "/" + file)
    # 移动文件到目录下
    file_path = path + "/" + file
    cmd = "cp -r " + meida_path + " " + file_path
    os.system(cmd)
    back.progress = 50
    back.save()
    sql_cmd = f"mysqldump -u{mysql_username} -p{mysql_pwd} {db} > {file_path}/db1.sql"
    os.system(sql_cmd)
    zip_cmd = "zip -r -m -P yth@!@#qzmp " + file + ".zip " + file
    os.system('cd backups && ' + zip_cmd)
    back.progress = 100
    back.status = 1
    back.backup_filepath = file_path + ".zip"
    back.save()
