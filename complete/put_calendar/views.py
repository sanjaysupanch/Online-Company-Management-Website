from django.shortcuts import render,HttpResponse
from put_calendar.models import check_date,check_date1
import datetime
import calendar

from django.contrib.auth.models import User
from accounts.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import check_date
from . serializers import check_dateSerializer,UserSerializer
from django.contrib.auth.models import User

from rest_framework import generics

from put_calendar.forms import check_dateform,choose_month_and_year_form




#from first_app.forms import calendar_data
# Create your views here.
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


def hello(request,select,show):


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

    mandy=choose_month_and_year_form()


    if select != '1':

        trig= select.split('m')

        print (trig)

        year= int(trig[0])
        month= int(trig[1])

        if int(show)<10:
            sdate = '0'+str(show)

        else:
            sdate= str(show)

        if int(month)<10:
            smonth = '0'+str(month)

        else:
            smonth= str(month)

        final_date = str(year)+'-'+str(smonth)+'-'+str(sdate)


        if request.method == 'POST':
            form = check_dateform(request.POST)

            if form.is_valid():
                 form_instance = form.save(commit=False)
                 form_instance.user=request.user
                 form_instance.date=final_date
                 form_instance.save()

                 form=check_dateform()


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
                if month<10:
                    c = str(str(year)+'-0'+str(month)+'-'+p[i])
                else:
                    c = str(str(year) + '-' + str(month) + '-' + p[i])
                q.append(c)

            dates_with_works = []
            work_on_date = []
            for i in range(len_month):
                a = [0,0,0,0,0,0,0]
                b.append(a)


            dates_needed = []

            query = check_date.objects.filter(user=request.user,date=final_date).order_by('date')

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

            print('else')
            print(form)
            return render(request,'put_templates/date.html',{'year_no':str(year)+'m'+str(month),'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name,'form':form,'final_date':final_date,'events':query,'mandy':mandy})

        else:
            form=check_dateform()




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
                if month<10:
                    c = str(str(year)+'-0'+str(month)+'-'+p[i])
                else:
                    c = str(str(year) + '-' + str(month) + '-' + p[i])
                q.append(c)

            dates_with_works = []
            work_on_date = []
            for i in range(len_month):
                a = [0,0,0,0,0,0,0]
                b.append(a)


            dates_needed = []

            query = check_date.objects.filter(user=request.user,date=final_date).order_by('date')

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

            print('else')
            print(form)
            return render(request,'put_templates/date.html',{'year_no':str(year)+'m'+str(month),'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name,'form':form,'final_date':final_date,'events':query,'mandy':mandy})

    else:



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
            if month<10:
                c = str(str(year)+'-0'+str(month)+'-'+p[i])
            else:
                c = str(str(year) + '-' + str(month) + '-' + p[i])
            q.append(c)

        dates_with_works = []
        work_on_date = []
        for i in range(len_month):
            a = [0,0,0,0,0,0,0]
            b.append(a)


        dates_needed = []

        query = check_date.objects.order_by('work_title')

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

        print('else')
        return render(request,'put_templates/date.html',{'year_no':str(year)+'m'+str(month),'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name,'mandy':mandy})









def date(request,select,show):
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


def date1(request,select,show):
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

def choose_event(request,select,show):

    if request.method == 'POST':

        form = choose_month_and_year_form(request.POST)


        month=int(request.POST['month'])
        year=int(request.POST['year'])



        return grid(request,year,month)



def grid(request,year,month):

    mandy=choose_month_and_year_form()

    if request.method == 'POST':
        form = check_dateform(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user=request.user
            form_instance.save()

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
                if month_calendar[i][j] < 10:
                    y = str('0'+str(month_calendar[i][j]))
                    p.append(y)
                if month_calendar[i][j] >= 10:
                    y = str(month_calendar[i][j])
                    p.append(y)

        q = []
        work_on_date = []
        for i in range(len(p)):
            if month<10:
                c = str(str(year)+'-0'+str(month)+'-'+p[i])
            else:
                c = str(str(year) + '-' + str(month) + '-' + p[i])
            q.append(c)

        for i in range(len_month):
            a = [0,0,0,0,0,0,0]
            b.append(a)

        query = check_date.objects.all()


        for i in range(len(query)):
            s = str(query[i].work_title)
            work_on_date.append(s)
            c = query[i].date
            d = c.isoformat()
            dates_needed.append(d)
            dates_with_works.append(int(d[8:10]))

        print(dates_needed)

        for m in range(len(q)):
          for i in range(len(b)):
            for j in range(len(b[i])):
                for k in range(len(dates_with_works)):
                   if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                       b[i][j] = [dates_with_works[k],work_on_date[k]]


        return render(request,'put_templates/date.html',{'year_no':str(year)+'m'+str(month),'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name,'mandy':mandy})

    else:
        form = check_dateform()

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
                if month_calendar[i][j] < 10:
                    y = str('0'+str(month_calendar[i][j]))
                    p.append(y)
                if month_calendar[i][j] >= 10:
                    y = str(month_calendar[i][j])
                    p.append(y)

        q = []
        work_on_date = []
        for i in range(len(p)):
            if month<10:
                c = str(str(year)+'-0'+str(month)+'-'+p[i])
            else:
                c = str(str(year) + '-' + str(month) + '-' + p[i])
            q.append(c)

        for i in range(len_month):
            a = [0,0,0,0,0,0,0]
            b.append(a)

        query = check_date.objects.all()


        for i in range(len(query)):
            s = str(query[i].work_title)
            work_on_date.append(s)
            c = query[i].date
            d = c.isoformat()
            dates_needed.append(d)
            dates_with_works.append(int(d[8:10]))

        #print(dates_with_works)



        print(dates_needed)

        for m in range(len(q)):
          for i in range(len(b)):
            for j in range(len(b[i])):
                for k in range(len(dates_with_works)):
                   if month_calendar[i][j] == dates_with_works[k] and q[m] == dates_needed[k]:
                       b[i][j] = [dates_with_works[k],work_on_date[k]]

        print("my name is laxman ssss")
        print(form)
        return render(request,'put_templates/date.html',{'year_no': str(year)+'m'+str(month),'month_cal':month_calendar,'zipped_data':zip(month_calendar,b),'present_year':year_name,'mandy':mandy})



def event_enter(request,date_selected):
    if request.method == 'POST':
        form = check_dateform(request.POST)

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user=request.user
            form_instance.save()

    else:
        form=check_dateform()
    return render(request,'put_templates/date.html',{'form':form})

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
