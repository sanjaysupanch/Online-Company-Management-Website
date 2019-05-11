from django.shortcuts import render, get_object_or_404,redirect
from .models import ClientList
from .forms import Clientform
from accounts.models import *

def client_create_view(request):
    form =Clientform(request.POST or None)
    if form.is_valid():
        form_instance=form.save(commit=False)
        form_instance.company_name=request.user.userprofile.company_name
        form_instance.save()
        return redirect('clients:index')

    context ={'form':form}
    return render(request,'clients/clients_create.html' ,context)
def index(request):
    all_clients = ClientList.objects.filter(company_name=request.user.userprofile.company_name)
    return render(request, 'clients/index1.html', {'all_clients':all_clients,})
