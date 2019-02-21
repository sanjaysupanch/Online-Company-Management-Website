from __future__ import print_function

from django.shortcuts import render,HttpResponse,redirect
from accounts.forms  import(
 RegistrationForm,customregcompany,
 regcompany,regteam,adduserform,todoform,assign_work,notify_work,uploadfileform,
EditProfileForm,customreg , ChangeProfileForm)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserProfile,teamtable,Todolist,GroupUserTable,upload_file,foldertable,filetable
from history.models import recent_activity

from django.core.files.storage import FileSystemStorage



# Create your views here.

from googleapiclient.discovery import build
from httplib2 import Http
import httplib2
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from apiclient import discovery
import os,io


SCOPES = 'https://www.eachgrpgoogleapis.com/auth/drive'

cwd = os.getcwd()

token=str(cwd)+'/accounts/token.json'
credit=str(cwd)+'/accounts/credentials.json'



store = file.Storage(token)
print(store)
creds = store.get()
print(creds)
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(credit, SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))



# Create your views here.

def index(request):
    return render(request,'accounts/testhome.html')
@login_required
def home(request):
    if request.method=='POST':
        form=regteam(request.POST)

        groups=GroupUserTable.objects.filter(user_name=request.user)

        if form.is_valid():
            form_instance=form.save(commit=False)
            form_instance.company_name=request.user.userprofile.company_name
            form_instance.save()

            ceo=UserProfile.objects.get(Jobtitle='CEO',company_name=request.user.userprofile.company_name)

            team_details=teamtable.objects.last()
            GroupUserTable.objects.create(user_name=ceo.user,team_details=team_details)

            if request.user.userprofile.Jobtitle != 'CEO':
                GroupUserTable.objects.create(user_name=request.user,team_details=team_details)

            form=regteam()
            message="successfully created "+str(request.POST['group_name'])+" group "
            args={'form':form,'message':message,'groups':groups}
            return render(request,'accounts/home.html',args)
        else:
            return HttpResponse("errors")

    else:
        form=regteam()


        groups=GroupUserTable.objects.filter(user_name=request.user)

        args={'form':form,'groups':groups}
        return render(request,'accounts/home.html',args)

def inter_reg(request):
    return render(request,'accounts/inter-reg.html')


def register(request):
     if request.method=='POST':
         form1=RegistrationForm(request.POST)
         form=customreg(request.POST)
         if form1.is_valid():
             if request.POST['Jobtitle'] != 'CEO':
                 form1_instance=form1.save()
                 form_instance=form.save(commit=False)

                 form_instance.user=form1_instance

                 form_instance.save()

                 return redirect('/accounts')
             else:
                 return HttpResponse("CEO should register with company ")
         else:
             return HttpResponse("form 1 is invalid")

     else:
         form=customreg()
         form1=RegistrationForm()
         args={'form':form,'form1':form1}
         #print(args[])
         return render(request,'accounts/reg_form.html',args)

def registercompany(request):
     if request.method=='POST':
         form1=RegistrationForm(request.POST)
         form=customregcompany(request.POST)
         form2=regcompany(request.POST)
         if form1.is_valid() and form.is_valid() and form2.is_valid():

             if request.POST['Jobtitle'] == 'CEO':
                 form2_instance=form2.save()
                 form1_instance=form1.save()
                 form_instance=form.save(commit=False)

                 form_instance.user=form1_instance
                 form_instance.company_name=form2_instance

                 form_instance.save()

                 return redirect('/accounts')
             else:
                 return HttpResponse("only ceo can register ")
         else:
             return HttpResponse("form 1 is invalid")

     else:
         form=customregcompany()
         form1=RegistrationForm()
         form2=regcompany()
         args={'form':form,'form1':form1,'form2':form2}
         #print(args[])
         return render(request,'accounts/reg_company.html',args)


@login_required
def view_profile(request,pk=None):
    if pk:
        user=User.objects.get(pk=pk)
    else:
        user=request.user
    args={'user':user}
    return render(request,'accounts/profile.html',args)


@login_required
def edit_profile(request):        #edit profile view
    if request.method=='POST':
        form=EditProfileForm(request.POST,instance=request.user)
        form1=ChangeProfileForm(request.POST,instance=request.user)
        #UserProfile.objects.filter(user=request.user).update(description='good_game')
        if form.is_valid() and form1.is_valid():
            form.save()
            UserProfile.objects.filter(user=request.user).update(description=request.POST['description'])
            UserProfile.objects.filter(user=request.user).update(city=request.POST['city'])
            UserProfile.objects.filter(user=request.user).update(phone=request.POST['phone'])
            return redirect('/accounts/profile')
        else:
            return HttpResponse("form  is invalid")

    else:
        form=EditProfileForm(instance=request.user)
        form1=ChangeProfileForm(request.POST,instance=request.user)
        args={'form':form,'form1':form1}
        return render(request,'accounts/edit_profile.html',args)


@login_required
def change_password(request):        #change password view
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')

    else:
        form=PasswordChangeForm(user=request.user)

        args={'form':form}
        return render(request,'accounts/change_password.html',args)

@login_required
def create_team(request):        #create team view
    if request.method=='POST':
        form=regteam(request.POST)
        if form.is_valid():
            form_instance=form.save(commit=False)
            form_instance.company_name=request.user.userprofile.company_name
            k=form_instance.save()
            return HttpResponse("successfully created a group")
        else:
            return HttpResponse("errors")

    else:
        form=regteam()

        args={'form':form}
        return render(request,'accounts/create_team.html',args)



@login_required
def add_user_team(request):        #change password view
    if request.method=='POST':
        form=adduserform(request.POST)
        if form.is_valid():
            username=request.POST['user_name']
            group_name=request.POST['group_name']
            team=teamtable.objects.get(company_name=request.user.userprofile.company_name,group_name=group_name)
            member=User.objects.get(username=username)
            print(team.id)
            GroupUserTable.objects.create(team_details=team,user_name=member)
            args={'form':form}
            render(request,'accounts/add_usertogroup.html',args)
        else:
            return HttpResponse("errors")

    else:
        form=adduserform()

        args={'form':form}
        return render(request,'accounts/add_usertogroup.html',args)

@login_required
def todo(request,pk):
    if pk:

        team=teamtable.objects.get(pk=pk)
        allist=Todolist.objects.filter(team_details=team)                                            #to do view
        if request.method=='POST':
            form=todoform(request.POST)
            form1=assign_work(request.POST)
            form2=notify_work(request.POST)
            if form.is_valid() and form1.is_valid() and form2.is_valid() :
                form_instance=form.save(commit=False)
                form_instance.user_name=request.user
                form_instance.team_details=team
                form_instance.save()
                form_instance1=form1.save(commit=False)
                form_instance1.work=form_instance
                form_instance1.save()
                form_instance2=form2.save(commit=False)
                form_instance2.work=form_instance
                form_instance2.save()

                return redirect("/accounts/todolists/"+str(pk)+'/')
            else:
                return HttpResponse("errors")

        else:
            team=teamtable.objects.get(pk=pk)
            allist=Todolist.objects.filter(team_details=team)                                            #to do view

            form=todoform()
            form1=assign_work()
            form2=notify_work()

            return render(request,'accounts/todolist.html',{'form':form,'form1':form1,'form2':form2,'alllist':allist})

@login_required
def view_group_with_pk(request,pk):        #add to do view
    if  pk:
            if request.method=='POST':
                form=adduserform(request.POST)
                team=teamtable.objects.get(pk=pk)
                Teammembers=GroupUserTable.objects.filter(team_details=team)

                if form.is_valid():
                    form_instance=form.save(commit=False)
                    form_instance.team_details=team
                    form_instance.save()
                    form=adduserform()
                    tm=form_instance.user_name

                    message="successfully added "+str(tm.username)+" to the team "
                    args={'form':form,'message':message,'members':Teammembers,'team':team}
                    return render(request,'accounts/view_individual_groups.html',args)
                else:
                    return HttpResponse("errors")

            else:
                form=adduserform()
                team=teamtable.objects.get(pk=pk)
                Teammembers=GroupUserTable.objects.filter(team_details=team)
                args={"members":Teammembers,'form':form,'team':team}

                return render(request,'accounts/view_individual_groups.html',args)

def fileupload(request,pk):
    if pk:
        if request.method=='POST':
            form=uploadfileform(request.POST,request.FILES)
            if form.is_valid():

                team=teamtable.objects.get(pk=pk)

                folder=foldertable.objects.get(team_details=team)

                folderid=str(folder.folderid)

                uploading=request.FILES['upload']
                print(type(uploading))
                print(uploading.temporary_file_path())

                folder_id = folderid

                file_metadata = {'name': str(uploading),'parents': [folder_id]}
                media = MediaFileUpload(str(uploading.temporary_file_path()),
                                    mimetype='image/jpeg',resumable=True)
                file1 = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()

                print ('File ID: %s' % file1.get('id'))

                fileid=file1.get('id')

                filetable.objects.create(parentfolder=folder,fileid=fileid,filename=str(uploading))

                return redirect('/accounts/uploadfilepath/'+str(pk)+'/')
            else:
                return HttpResponse("errors")

        else:
            team=teamtable.objects.get(pk=pk)
            folder=foldertable.objects.get(team_details=team)
            allfiles=filetable.objects.filter(parentfolder=folder)

            form=uploadfileform()
            args={'form':form,'files':allfiles}
            return render(request,'accounts/uploadfile.html',args)

def filedownload(request,pk):
    if pk:
        file=filetable.objects.get(pk=pk)
        file_id = str(file.fileid)
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))

        filepath='/home/laxman/Downloads/'+str(file.filename)
        with io.open(filepath,'wb') as f:
            fh.seek(0)
            f.write(fh.read())

        return HttpResponse('successfully downloaded a file')
@login_required
def list_activities(request):
    user = request.user.userprofile.company_name
    users = UserProfile.objects.filter(company_name=user)
    return render(request, 'accounts/list_activities.html', {'users': users})


def specific_activities(request,pk):
    user=User.objects.get(pk=pk)
    print(user)
    last_task = recent_activity.objects.filter(user=user).order_by('-dates')
    task_dict = {"trials": last_task,"user":user}
    return render(request, 'accounts/specific_activities.html', task_dict)
