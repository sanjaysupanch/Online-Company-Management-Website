from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from accounts.models import *
from django.contrib.auth.models import User
from accounts.models import Company,teamtable

# Create your models here.
class ClientList(models.Model):
    name = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    phno = models.CharField(max_length=10,validators=[RegexValidator(regex='^.{10}$',message='length has to be 10', code='nomatch')])
    email = models.EmailField('Email', max_length=150)
    team_details=models.ForeignKey(teamtable,on_delete=models.CASCADE,default='')
    company_name=models.ForeignKey(Company,on_delete=models.CASCADE,default='')

    class Meta:
        unique_together = ['name','phno','email']

    def __str__(self):
        return self.name
