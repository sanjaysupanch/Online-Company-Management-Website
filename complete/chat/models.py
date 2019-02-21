from django.db import models
from django.contrib.auth.models import User


from accounts.models import teamtable

from django.dispatch import receiver
from django.db.models.signals import post_save

class Room(models.Model):

    # Room title
    title = models.CharField(max_length=255)

    teamdetails=models.ForeignKey(teamtable,on_delete =models.CASCADE,default='')


    def __str__(self):
        return self.title

    @property
    def group_name(self):
        return "room-%s" % self.id

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete =models.CASCADE)
    group = models.ForeignKey(Room,on_delete =models.CASCADE)
    body = models.CharField(max_length = 50)
    time = models.DateTimeField()
    def json(self):
        return {
            'user' : self.user,
            'group' : self.group,
            'body' : self.body,
        }

@receiver(post_save,sender=teamtable)
def add_todo_to_cal(sender,instance,created,**kwargs):
    if created:
        Room.objects.create(
                    title=str(instance.group_name),
                    teamdetails= instance,

        )
