
from django.http import Http404,HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from blog.models import post, comment
from .forms import postform, commentform
from django.shortcuts import redirect
from accounts.models import teamtable


# Create your views here.

def index(request,pk):
    if pk:
        team=teamtable.objects.get(pk=pk)
        pindex = post.objects.filter(team_details=team).order_by('-timestamp')
        posts_dict_index = {'posts': pindex,'team': team}

        return render(request, 'blog/index.html', posts_dict_index)
    else:
        return HttpResponse("excellent")

def details(request, pk):
    posts = get_object_or_404(post,id=pk)
    comments = comment.objects.filter(post=posts)
    posts_dict_details = {'posts':posts, 'allcomments': comments}
    return render(request, 'blog/details.html', posts_dict_details)


def newpost(request,pk=3):

    if request.method == "POST":
        newform = postform(request.POST)
        if newform.is_valid():
            new_post = newform.save(commit=False)
            title=request.POST['title']
            content=request.POST['content']
            new_post.author = request.user
            new_post.published_date = timezone.now()
            teaming=teamtable.objects.get(pk=pk)
            print(teaming)
            newpost.team_details=teaming
            new_post.save()
            post.objects.create(title=title,content=content,author=request.user,team_details=teaming)
            return redirect('/blog/show/'+str(pk)+'/')
    else:
        newform = postform()
        return render(request, 'blog/newpost.html', {'form': newform})


def editpost(request, pk):
    posts = get_object_or_404(post, pk=pk)
    if posts.author != request.user:
        raise Http404()

    if request.method == "POST":
        editform = postform(request.POST, instance=posts)
        if editform.is_valid():
            edit_post = editform.save(commit=False)
            edit_post.published_date = timezone.now()
            team=edit_post.team_details
            edit_post.save()
            teamid=team.pk

            return redirect('/blog/show/'+str(teamid)+'/')

    else:
        editform = postform(instance=posts)
        return render(request, 'blog/editpost.html', {'form': editform})


def deletepost(request, pk):
    posts = get_object_or_404(post, pk=pk)
    if posts.author != request.user:
        raise Http404()
    team=posts.team_details
    teamid=team.pk
    posts.delete()
    return redirect('/blog/show/'+str(teamid)+'/')

def addcomment(request, pk):
    posts = get_object_or_404(post,pk=pk)
    if request.method == 'POST':
        com_form=commentform(request.POST)
        if com_form.is_valid():
            comment_var =com_form.save(commit=False)
            comment_var.post=posts
            comment.author=request.user
            comment_var.save()
            postid=posts.pk
            return redirect('/blog/post/'+str(postid)+'/')
    else:
        com_form = commentform()
    return render(request, 'blog/addcomment.html',{'form':com_form})
