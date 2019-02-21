from django.shortcuts import render, redirect
from .models import TaskList, MyTodoList
from django.utils import timezone
from .forms import MyTodoform

from django.contrib import messages

# Create your views here.

def display_view(request):
    all_tasks = TaskList.objects.filter(user=request.user)
    all_tasks.order_by('-created').reverse()
    rev_all_tasks = list(reversed(all_tasks))
    return render(request, 'assignments/display.html', {'all_tasks':rev_all_tasks})

def my_todo_view(request):
    all_todo = MyTodoList.objects.filter(user=request.user)
    all_todo.reverse()
    rev_all_todo = list(reversed(all_todo))
    return render(request, 'assignments/my_todo.html',{'all_todo':rev_all_todo})

def delete_tasks(request,task_id):
    item = TaskList.objects.get(pk = task_id)
    item.delete()
    return redirect('assignments:display')

def update_tasks(request,task_id):
    item = TaskList.objects.get(pk = task_id)
    item.done = True
    item.time_of_submission = timezone.now()
    item.save()
    return redirect('assignments:display')


def add_todo_list_view(request):
    form =MyTodoform(request.POST or None)
    if form.is_valid():
        forminstance=form.save(commit=False)
        forminstance.user=request.user
        forminstance.save()
        return redirect('assignments:my_todo')
    context ={'form':form}
    return render(request,'assignments/add_todo.html' ,context)

def delete_todo(request,todo_id):
    item = MyTodoList.objects.get(pk = todo_id)
    item.delete()
    return redirect('assignments:my_todo')


def update_todo(request,todo_id):
    item = MyTodoList.objects.get(pk = todo_id)
    item.done = True
    item.save()
    return redirect('assignments:my_todo')
