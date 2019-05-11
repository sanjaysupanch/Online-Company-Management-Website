from django.db import models
from accounts.models import *
from django.contrib.auth.models import User

# Create your models here.
class NotificationList(models.Model):
    message = models.CharField(max_length=250)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
