from django.db import models

# Create your models here.
from user.models import UserInfo

from taskmanage.models import Task, File


class MindMap(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_mind_map'


class MindNode(models.Model):
    mind = models.ForeignKey(MindMap, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=125, null=True)
    node_type = models.IntegerField(default=1)  # 1是IP  2是网段  3是域名 4是其他
    ascription = models.CharField(max_length=128, null=True)
    os = models.CharField(max_length=128, null=True)
    note = models.TextField(null=True)
    left = models.BooleanField(default=True)
    child = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    index = models.IntegerField(default=0)

    def get_sub_note(self):
        return MindNode.objects.filter(child=self).order_by("index")


class NodeFile(models.Model):
    node = models.ForeignKey(MindNode, on_delete=models.CASCADE, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True)


class OpenDir(models.Model):
    node = models.ForeignKey(MindNode, on_delete=models.CASCADE, null=True)
    dir = models.TextField(null=True)


class MindLog(models.Model):
    action = models.IntegerField(verbose_name='执行动作', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    mind_name = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)


class MindOnlineUser(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    mind = models.ForeignKey(MindMap, on_delete=models.CASCADE)


class MindNodeLog(models.Model):
    action = models.IntegerField(verbose_name='执行动作', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    mind = models.ForeignKey(MindMap, on_delete=models.CASCADE, null=True)
    node_name = models.CharField(max_length=50, null=True)
