from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.contrib import messages
from validate_email import validate_email

# Create your views here.


def logout_view(request):
    """logging out users"""
    logout(request)
    return HttpResponseRedirect(reverse('blogs:home'))


def register_view(request):
    """register new user"""

    if request.method == 'POST':
        
        #user submitted data processing
        context = {"has_error" : False, "data" : request.POST}
        username = request.POST.get("Username")
        password1 = request.POST.get("Password1")
        password2 = request.POST.get("Password2")
        email = request.POST.get("email")

        if not username:
            messages.add_message(request, messages.ERROR, "Username is required")
            context["has_error"] = True 

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username already exists")
            context["has_error"] = True
        
        if len(password1) < 6:
            messages.add_message(request, messages.ERROR, "Password must be atleast 6 characters long")
            context["has_error"] = True
        
        if password1 != password2:
            messages.add_message(request, messages.ERROR, "Password mismatch")
            context["has_error"] = True
        
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, "Email isnt valid")
            context["has_error"] = True
        
        if User.objects.filter(email=email):
            messages.add_message(request, messages.ERROR, "Email is already used")
            context["has_error"] = True

        if context["has_error"]:
            return render(request, 'register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()


        messages.add_message(request, messages.SUCCESS, "New User Registered")        
        return HttpResponseRedirect(reverse('users:login'))
    else:

        # initial get request new form
        #form = SignUpForm()
        return render(request, 'register.html')


def login_view(request):
    """login user"""

    if request.method != "POST":
        # intial get request
        return render(request, 'login.html')
    else:
        context = {'data' : request.POST}
        username = request.POST.get("Username")
        password = request.POST.get("Password")

        user = authenticate(request, username = username, password = password)

        if not user:
            # user isnt registered
            messages.add_message(request, messages.ERROR, "Invalid Credentials")
            return render(request, "login.html")
        
        # logging in user
        login(request, user)
        
        messages.add_message(request, messages.SUCCESS, f"Welcome {user.username}")
        
        return HttpResponseRedirect(reverse('blogs:my_blogs'))


        