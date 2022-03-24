
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from users.forms import SignUpForm
# Create your views here.


def logout_view(request):
    """logging out users"""
    logout(request)
    return HttpResponseRedirect(reverse('blogs:home'))


def register_view(request):
    """register new user"""

    if request.method != 'POST':
        # initial get request new form
        form = SignUpForm()
    else:
        # user submitted data processing 
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username , password = request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('blogs:home'))
    context = {'form' : form}
    
    return render(request, 'register.html', context)


def login_view(request):
    """login user"""

    if request.method != "POST":
        # intial request
        return render(request, 'login.html')
    else:
        context = {'data' : request.form}
        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate(request, username = username, password = password)

        if not user:
            # user isnt registered
            return render("users:login", message="Invalid credentials")
        
        