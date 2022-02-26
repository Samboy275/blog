from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def logout_view(request):
    """logging out users"""
    logout(request)
    return HttpResponseRedirect(reverse('blogs:home'))


def register_view(request):
    """register new user"""

    if request.method != 'POST':
        # initial get request new form
        form = UserCreationForm()
    else:
        # user submitted data processing 
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username , password = request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('blogs:home'))
    context = {'form' : form}
    
    return render(request, 'register.html', context)
