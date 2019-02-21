from django.shortcuts import render,HttpResponse
from put_calendar.models import check_date,check_date1
import datetime
import calendar
from .forms import EventForm,GroupForm
from django.contrib.auth.models import User
from accounts.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import check_date
from . serializers import check_dateSerializer,UserSerializer
from django.contrib.auth.models import User

from rest_framework import generics



#from first_app.forms import calendar_data
# Create your views here.
next_m = 0
next_y = 0
back_m = 0
back_y = 0


def currentdate():
    return datetime.date.today()




def index(request):
    return render(request,'put_calendar/index.html')

def hello(request):
    x = currentdate()
    y = x.isoformat()
    year = int(y[:4])
    month = int(y[5:7])
    global next_m
    next_m = month
    global next_y
    next_y = year
    global back_m
    back_m = month
    global back_y

    back_y = year
    month_calendar = calendar.monthcalendar(year,month)

    month_name = calendar.month_name[month]
    year_name = str(month_name + ' , '+str(year))
    len_month = len(month_calendar)

    p = []
    b = []

    for i in range(len(month_calendar)):
     for j in range(len(month_calendar[i])):
        if month_calendar[i][j] > 0:
            if month_calendar[i][j] <10:
                y = str('0'+str(month_calendar[i][j]))
                p.append(y)
            if month_calendar[i][j] >= 10:
                y = str(month_calendar[i][j])
                p.append(y)

    q = []
    for i in range(len(p)):
        c = str(str(year)+'-'+str(month)+'-'+p[i])
        q.append(c)

    dates_with_works = []
    work_on_date = []
    for i in range(len_month):
        a = [0,0,0,0,0,0,0]
        b.append(a)


    dates_needed = []

    query = check_date.objects.filter(user=request.user).order_by('work_title')

    for i in range(len(query)):
        s =str(query[i].work_title)
        work_on_date.append(s)
        c = query[i].date
        d = c.isoformat()
        dates_needed.append(d)
        dates_with_works.append(int(d[8:10]))

    for m in range(len(q)):
      for i in range(len(b)):
        for j in range(len(b[i])):
            for k in range(len(dates_with_works)):
               if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                   b[i][j] = [dates_with_works[k],work_on_date[k]]


    return render(request,'put_templates/date.html',{'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name})


def date(request):
    global back_m
    global back_y
    global next_m
    global next_y
    if next_m <12 and next_m >= 1:
       next_m = next_m + 1
       next_y = next_y
    else :
       next_m = 1
       next_y = next_y +1
    back_m = next_m
    back_y = next_y
    print(next_m,next_y)
    return grid(request,next_y,next_m)


def date1(request):
    global back_m
    global back_y
    global next_m
    global next_y
    if back_m >1 and back_m <=12:
       back_m = back_m - 1
       back_y = back_y
    else :
       back_m = 12
       back_y = back_y - 1
    next_m = back_m
    next_y = back_y
    return grid(request,back_y,back_m)


def grid(request,year,month):
    month_calendar = calendar.monthcalendar(year,month)
    month_name = calendar.month_name[month]
    year_name = str(month_name + ' , '+str(year))

    len_month = len(month_calendar)

    b = []
    dates_with_works = []
    dates_needed = []
    p = []
    for i in range(len(month_calendar)):
     for j in range(len(month_calendar[i])):
        if month_calendar[i][j] > 0:
            if month_calendar[i][j] <10:
                y = str('0'+str(month_calendar[i][j]))
                p.append(y)
            if month_calendar[i][j] >= 10:
                y = str(month_calendar[i][j])
                p.append(y)

    q = []
    work_on_date = []
    for i in range(len(p)):
        c = str(str(year)+'-'+str(month)+'-'+p[i])
        q.append(c)

    for i in range(len_month):
        a = [0,0,0,0,0,0,0]
        b.append(a)

    query = check_date.objects.order_by('work_title')

    for i in range(len(query)):
        s = str(query[i].work_title)
        work_on_date.append(s)
        c = query[i].date
        d = c.isoformat()
        dates_needed.append(d)
        dates_with_works.append(int(d[8:10]))
    for m in range(len(q)):
      for i in range(len(b)):
        for j in range(len(b[i])):
            for k in range(len(dates_with_works)):
               if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                   b[i][j] = [dates_with_works[k],work_on_date[k]]

    return render(request,'put_templates/date.html',{'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name})


def create_event(request):
    form = EventForm(request.POST or None)
    if form.is_valid():

        date = request.POST['date']
        work_title = request.POST['work_title']

        present_user=request.user
        print(present_user)
        x=UserProfile.objects.get(user=present_user)
        print(x)

        company=x.company_name.company_name
        print(company)
        all_users=UserProfile.objects.filter(company_name=company)
        print(all_users)
        for user_x in all_users:
            check_date.objects.create(date=date,work_title=work_title,user=user_x.user)
        return HttpResponse('event added')


    context = {'form': form}
    return render(request, 'put_templates/events_create.html', context)




def group_hello(request):
    x = currentdate()
    y = x.isoformat()
    year = int(y[:4])
    month = int(y[5:7])
    global next_m
    next_m = month
    global next_y
    next_y = year
    global back_m
    back_m = month
    global back_y

    back_y = year
    month_calendar = calendar.monthcalendar(year,month)

    month_name = calendar.month_name[month]
    year_name = str(month_name + ' , '+str(year))
    len_month = len(month_calendar)

    p = []
    b = []

    for i in range(len(month_calendar)):
     for j in range(len(month_calendar[i])):
        if month_calendar[i][j] > 0:
            if month_calendar[i][j] <10:
                y = str('0'+str(month_calendar[i][j]))
                p.append(y)
            if month_calendar[i][j] >= 10:
                y = str(month_calendar[i][j])
                p.append(y)

    q = []
    for i in range(len(p)):
        c = str(str(year)+'-'+str(month)+'-'+p[i])
        q.append(c)

    dates_with_works = []
    work_on_date = []
    for i in range(len_month):
        a = [0,0,0,0,0,0,0]
        b.append(a)


    dates_needed = []

    query = check_date1.objects.order_by('work_title')

    for i in range(len(query)):
        s =str(query[i].work_title)
        work_on_date.append(s)
        c = query[i].date
        d = c.isoformat()
        dates_needed.append(d)
        dates_with_works.append(int(d[8:10]))

    for m in range(len(q)):
      for i in range(len(b)):
        for j in range(len(b[i])):
            for k in range(len(dates_with_works)):
               if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                   b[i][j] = [dates_with_works[k],work_on_date[k]]


    return render(request,'put_templates/date.html',{'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name})


def group_date(request):
    global back_m
    global back_y
    global next_m
    global next_y
    if next_m <12 and next_m >= 1:
       next_m = next_m + 1
       next_y = next_y
    else :
       next_m = 1
       next_y = next_y +1
    back_m = next_m
    back_y = next_y
    print(next_m,next_y)
    return group_grid(request,next_y,next_m)


def group_date1(request):
    global back_m
    global back_y
    global next_m
    global next_y
    if back_m >1 and back_m <=12:
       back_m = back_m - 1
       back_y = back_y
    else :
       back_m = 12
       back_y = back_y - 1
    next_m = back_m
    next_y = back_y
    return group_grid(request,back_y,back_m)


def group_grid(request,year,month):
    month_calendar = calendar.monthcalendar(year,month)
    month_name = calendar.month_name[month]
    year_name = str(month_name + ' , '+str(year))

    len_month = len(month_calendar)

    b = []
    dates_with_works = []
    dates_needed = []
    p = []
    for i in range(len(month_calendar)):
     for j in range(len(month_calendar[i])):
        if month_calendar[i][j] > 0:
            if month_calendar[i][j] <10:
                y = str('0'+str(month_calendar[i][j]))
                p.append(y)
            if month_calendar[i][j] >= 10:
                y = str(month_calendar[i][j])
                p.append(y)

    q = []
    work_on_date = []
    for i in range(len(p)):
        c = str(str(year)+'-'+str(month)+'-'+p[i])
        q.append(c)

    for i in range(len_month):
        a = [0,0,0,0,0,0,0]
        b.append(a)

    query = check_date1.objects.order_by('work_title')

    for i in range(len(query)):
        s = str(query[i].work_title)
        work_on_date.append(s)
        c = query[i].date
        d = c.isoformat()
        dates_needed.append(d)
        dates_with_works.append(int(d[8:10]))
    for m in range(len(q)):
      for i in range(len(b)):
        for j in range(len(b[i])):
            for k in range(len(dates_with_works)):
               if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                   b[i][j] = [dates_with_works[k],work_on_date[k]]

    return render(request,'put_templates/date.html',{'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name})



def create_group(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():

        date = request.POST['date']
        work_title = request.POST['work_title']
        team_details=request.POST['team_details']
        '''team=GroupUserTable.objects.get(user_name=request.user)
        print(team)
        group=team.team_details.group_name
        print(group)

        group_t=teamtable.objects.get(group_name=group)
        print(group_t)'''

        form.save()
        #check_date1.objects.create(date=date, work_title=work_title,team_details=team_details)
        return HttpResponse('form filled')

    context = {'form': form}
    return render(request, 'put_templates/events_create.html', context)


class DatesListView(generics.ListCreateAPIView):
    queryset = check_date.objects.all()
    serializer_class = check_dateSerializer

class DatesFilterView(generics.ListCreateAPIView):

    serializer_class = check_dateSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        #user = self.request.user
        user = self.kwargs['pk']
        return check_date.objects.filter(user=user)


class DatesView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = check_dateSerializer
    queryset = check_date.objects.all()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
