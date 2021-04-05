from django.db import models

from mind.models import MindNode
from taskmanage.models import Task

from user.models import UserInfo

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


class TaskProgress(models.Model):
    name = models.CharField(max_length=128)
    update_time = models.DateTimeField(null=True)
    weight = models.IntegerField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Host(models.Model):
    name = models.CharField(max_length=128, default="未知")
    ip = models.CharField(max_length=128)
    os_info = models.CharField(max_length=128, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
    node = models.ForeignKey(MindNode, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'tb_host'
        verbose_name = '主机表'


class TaskVulnerability(models.Model):
    name = models.CharField(max_length=128)
    describe = models.TextField(null=True)
    level = models.IntegerField()  # 1是低 2是中 3是高
    quote = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'tb_task_vulnerability'
        verbose_name = '任务漏洞表'


class TaskCertificate(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'tb_task_certificate'
        verbose_name = '凭证列表'


class TaskPort(models.Model):
    name = models.CharField(max_length=128, null=True)
    port = models.CharField(max_length=128)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    node = models.ForeignKey(MindNode, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'tb_task_port'
        verbose_name = '端口列表'


class OperatingLog(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=True)  # 操作内容
    operator_id = models.IntegerField()  # 操作人id

    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_operating_log'


# 数据备份记录/进度
class BackupRecord(models.Model):
    id = models.AutoField(primary_key=True)
    progress = models.IntegerField(default=0)  # 数值区间[0,100]
    backup_filepath = models.TextField(null=True)  # 备份文件路径
    status = models.IntegerField(default=0)  # 0是备份中 1是备份成功 2是备份失败
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_backup_record'


class ServerPort(models.Model):
    server = models.CharField(max_length=155, null=True)
    port = models.IntegerField()

    class Meta:
        db_table = 'tb_server_port'
