from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
import httplib2
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from apiclient import discovery
import os,io
from django.dispatch import receiver
from django.db.models.signals import post_save



# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


##google drive api modules



from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User


CHOICES = (
    ('CEO','CEO'),
    ('Project Manager', 'Project Manager'),
    ('Employee','Employee'),
)

# Create your models here.{Database Table models}

class Company(models.Model): #[Table of companies ]
    company_name=models.CharField(max_length=100,default='',primary_key=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.PROTECT) #or models.CASCADE
    Jobtitle=models.CharField(max_length=100,default='',choices=CHOICES)
    city=models.CharField(max_length=100,default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='image_profile',blank=True)
    company_name=models.ForeignKey(Company,default='',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class teamtable(models.Model):

    company_name=models.ForeignKey(Company,default='',on_delete=models.CASCADE)
    group_name=models.CharField(max_length=100,default='')

    class Meta:
        unique_together = (('company_name', 'group_name'),)
    def __str__(self):
        return self.group_name



class GroupUserTable(models.Model):
    team_details=models.ForeignKey(teamtable,default='',on_delete=models.CASCADE)
    user_name=models.ForeignKey(User,default='',on_delete=models.CASCADE)
    class Meta:
        unique_together = (('team_details', 'user_name'),)
    def __str__(self):
        return str(self.team_details)


class Todolist(models.Model):
    status=models.BooleanField(default=False)
    title=models.CharField(max_length=250)
    project_name=models.CharField(max_length=250)

    description=models.CharField(max_length=100,default='')
    deadline=models.DateField(default=timezone.now)
    assigned=models.DateField(default=timezone.now)
    team_details=models.ForeignKey(teamtable,default='',on_delete=models.CASCADE)
    user_name=models.ForeignKey(User,default='',on_delete=models.CASCADE)

    class Meta:
        unique_together = (('title', 'user_name'),)

    def __str__(self):
        return self.title

class work_assigned(models.Model):
    work=models.ForeignKey(Todolist,default='',on_delete=models.CASCADE)
    user_assign=models.ForeignKey(User,default='',on_delete=models.CASCADE)
    def __str__(self):
        return self.work.title
class to_notify(models.Model):
    work=models.ForeignKey(Todolist,default='',on_delete=models.CASCADE)
    done=models.BooleanField(default=False)
    user_notify=models.ForeignKey(User,default='',on_delete=models.CASCADE)



class upload_file(models.Model):
    upload=models.FileField(upload_to='files')


class foldertable(models.Model):

    folderid=models.CharField(max_length=100,default='')
    foldername=models.CharField(max_length=100,default='')
    team_details=models.ForeignKey(teamtable,default='',on_delete=models.CASCADE)

    

    def __str__(self):
        return self.foldername




class filetable(models.Model):

    parentfolder=models.ForeignKey(foldertable,default='',on_delete=models.CASCADE)
    fileid=models.CharField(max_length=100,default='')
    filename=models.CharField(max_length=100,default='')



@receiver(post_save,sender=teamtable)
def createfolder(sender,instance,created,**kwargs):
    cwd = os.getcwd()

    token=str(cwd)+'/accounts/token.json'
    credit=str(cwd)+'/accounts/credentials.json'

    if created:
        store = file.Storage(token)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credit, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    foldername=str(instance.group_name)+'-->'+str(instance.company_name)

    file_metadata = {
    'name': foldername,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file1 = service.files().create(body=file_metadata,
                                    fields='id').execute()

    print ('Folder ID: %s' % file1.get('id'))

    folderid=file1.get('id')

    foldertable.objects.create(
                                folderid=folderid,
                                foldername = foldername,
                                team_details = instance

                                )
