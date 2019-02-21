from django.db import models
from django.utils import timezone
from accounts.models import *
from django.contrib.auth.models import User
from notifications.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from put_calendar.models import check_date

# Create your models here.
class TaskList(models.Model):
    title = models.CharField(max_length=250)
    project_name = models.CharField(max_length=250)
    description = models.TextField(blank=True,null=True)
    created = models.DateField()
    due_date = models.DateField()
    time_of_submission = models.DateField(blank=True,null=True)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    work = models.ForeignKey(Todolist,on_delete=models.CASCADE)


    class Meta:
        ordering = ['created']
        unique_together = ['title', 'project_name',]

class MyTodoList(models.Model):
    title = models.CharField(max_length=250)
    due_date =models.DateField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    class Meta:
        unique_together = ['title','due_date',]



@receiver(post_save, sender=MyTodoList)
def add_to_other(sender, instance,created,updated_fields='done', **kwargs):
    if created:
        NotificationList.objects.create(message=instance.title+'added in todo list',user=instance.user)
    elif updated_fields is 'done':
        NotificationList.objects.create(message=instance.title+'marked done',user=instance.user)


@receiver(post_save, sender=TaskList)
def add_to_another(sender, instance,created,updated_fields='done', **kwargs):
    if created:
        pass
    elif updated_fields is 'done':
        NotificationList.objects.create(message=instance.title+'marked done',user=instance.user)
        upstatus=Todolist.objects.filter(pk=instance.work.pk)
        upstatus.update(status=instance.done)
        '''upnotify=to_notify.objects.filter(work=instance.work)
        upnotify.update(done=instance.done)'''

@receiver(post_save,sender=work_assigned)
def assign_task(sender,instance,created,**kwargs):
    if created:
        qwe=Todolist.objects.get(pk=instance.work.pk)
        print(qwe)
        w=work_assigned.objects.get(pk=instance.pk)
        print(w.user_assign)
        NotificationList.objects.create(message=instance.work.title+'added in tasklist',user=instance.user_assign)
        print(w)
        TaskList.objects.create(
            title=instance.work.title,
            project_name=instance.work.project_name,
            description=instance.work.description,
            created=instance.work.assigned,
            due_date=instance.work.deadline,
            done=instance.work.status,
            user=instance.user_assign,
            work = qwe
        )


@receiver(post_save,sender=to_notify)
def notify_done(sender,instance,created,updated_fields='done',**kwargs):
    if created:
        NotificationList.objects.create(message='you assigned a new task',user=instance.user_notify)
    elif updated_fields is 'done':
        NotificationList.objects.create(message='task you assigned is done',user=instance.user_notify)


@receiver(post_save,sender=TaskList)
def add_to_cal(sender,instance,created,**kwargs):
    if created:
        check_date.objects.create(
            work_title=instance.title,
            date=instance.due_date,
            user=instance.user
        )

@receiver(post_save,sender=MyTodoList)
def add_todo_to_cal(sender,instance,created,**kwargs):
    if created:
        check_date.objects.create(
            work_title=instance.title,
            date=instance.due_date,
            user=instance.user
        )
