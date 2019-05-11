from django.test import TestCase

from accounts.models import *
from chat.models import *
from blog.models import *
from assignments.models import *
from clients.models import *
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from put_calendar.models import *
from django.urls import reverse
from django.test.client import Client
# Create your tests here.


class AccountTest(TestCase):

    def create_company(self,company_name="verygood testing"):
        return Company.objects.create(
                                    company_name=company_name,
                                )

    def test_company_creation(self):
        test_company = self.create_company()
        self.assertTrue(isinstance(test_company, Company))  #assertequal
        self.assertEqual(test_company.__str__(),test_company.company_name)

class AccountViewTestcase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username='test_user',password='ironman3',email='laxmankumarapu@gmail.com',first_name='lucky',last_name='good')
        user=cls.user

        company_name=Company.objects.create(company_name='spacex')
        userprofile=UserProfile.objects.create(user=user,Jobtitle='CEO',city='vizag',phone=134,company_name=company_name)

        teamtable1=teamtable.objects.create(company_name=company_name,group_name='marketing')

        grpusertable=GroupUserTable.objects.create(team_details=teamtable1,user_name=user)

        todolist=Todolist.objects.create(title='Do ase test',project_name='kickstart',description='ase1',team_details=teamtable1,user_name=user)

        workassigned=work_assigned.objects.create(work=todolist,user_assign=user)

        tonotify=to_notify.objects.create(work=todolist,user_notify=user)

        post1=post.objects.create(title='First post',content='text-field',author=user,team_details=teamtable1)

        comment1=comment.objects.create(post=post1,content='text-field',author=user)

        mytodolist=MyTodoList.objects.create(title='my work',due_date=timezone.now().date(),user=user)

        tasklist=TaskList.objects.create(title='my assignments',project_name='kickstart1',description='ase11',created=timezone.now().date(),due_date=timezone.now().date()

                                        ,user=user,work=todolist)

        clientlist=ClientList.objects.create(name='client-test',project_name='kickstart1',phno='1234567890',email='laxmankumarapu@gmail.com',team_details=teamtable1,
                                        company_name=company_name)

        recentactivity=recent_activity.objects.create(task_done='completed',user=user)

        checkdate=check_date.objects.create(date=timezone.now().date(),work_title='good morning',user=user)

        #folder=foldertable.objects.create(folderid='123',foldername='testfolder',team_details=teamtable1)

        #file=filetable.objects.create(parentfolder=folder,fileid='testfile123',filename='testfile',)

        #room=Room.objects.create(title='chat_test',teamdetails=teamtable1)

        #chat=Chat.objects.create(user=user,group=room,body='a message',time=timezone.now())



    return_status=302

    def test_view_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_view_register_user(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/reg_form.html')

    def test_view_register_company(self):
        response = self.client.get(reverse('registercompany'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/reg_company.html')

    def test_view_home(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')

    def test_view_profileview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_view_profileview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_view_editprofileview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')


    def test_view_changepasswordview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')


    def test_view_createteamview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('reg_team'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_team.html')

    def test_view_adduserteamview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('add_user_team'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/add_usertogroup.html')

    def test_view_team_todo_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('accounts.todo', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/todolist.html')

    def test_view_groupview(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('view_group_with_pk', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/view_individual_groups.html')

    def test_view_fileupload(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('file_upload', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/uploadfile.html')


    def test_view_chat(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('chat.group',  args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_blog_index(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('blog_index',  args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_view_blog_details(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('details',  args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/details.html')

    def test_view_newpost(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('newpost',  args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/newpost.html')

    def test_view_editpost(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('editpost',  args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/editpost.html')

    def test_view_addcomment(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('add-comment',  args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/addcomment.html')

    def test_display_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:display'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assignments/display.html')

    def test_my_todo_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:my_todo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assignments/my_todo.html')

    def test_add_todo_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:add_todo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assignments/add_todo.html')


    def test_delete_task_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:delete_task',args=[1]))
        self.assertEqual(response.status_code, self.return_status)
        self.assertRedirects(response, '/assignments/display/')


    def test_update_task_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:update_task',args=[1]))
        self.assertEqual(response.status_code, self.return_status)
        self.assertRedirects(response, '/assignments/display/')

    def test_delete_todo_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:delete_todo',args=[1]))
        self.assertEqual(response.status_code, self.return_status)
        self.assertRedirects(response, '/assignments/my_todo/')

    def test_update_todo_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('assignments:update_todo',args=[1]))
        self.assertEqual(response.status_code, self.return_status)
        self.assertRedirects(response, '/assignments/my_todo/')


    def test_client_create_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('clients:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/clients_create.html')

    def test_clients_index_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('clients:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/index1.html')

    def test_history_index_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('history:trials'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history/display.html')

    def test_index_notifications_view(self):
        self.client.login(username='test_user',password='ironman3')
        response=self.client.get(reverse('notifications:index'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'notifications/index.html')

    def test_notifs_update_view(self):
        self.client.login(username='test_user',password='ironman3')
        response=self.client.get(reverse('notifications:update',args=[1]))
        self.assertEqual(response.status_code,self.return_status)
        self.assertRedirects(response,'/notifications/')

    def test_date_view(self):
        self.client.login(username='test_user', password='ironman3')
        response = self.client.get(reverse('put_calendar:date'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'put_templates/date.html')
