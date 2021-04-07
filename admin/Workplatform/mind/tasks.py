from __future__ import absolute_import

from datetime import datetime

from celery import task, Task

from adminq.models import TaskProgress
from taskmanage.models import Task as TaskModel


from celery import shared_task

@task(name='update')
def update_task():
    task_list = TaskModel.objects.all()
    for task in task_list:
        print(task.end_time)
        if task.end_time <= datetime.now():
            task_id = task.id
            task_obj = TaskProgress.objects.filter(task_id=task_id, update_time__isnull=True)
            if task_obj.count() < 3:
                task_obj.update(update_time=datetime.now())
