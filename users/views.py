
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.contrib import messages
from validate_email import validate_email
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
# Create your views here.


class EmailThread(threading.Thread):


    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)


    def run(self):
        print("sending email")
        self.email.send

def send_verification_email(user, request):
    """Function to send a verification email to the user"""
    
    current_site = get_current_site(request)
    print(current_site)
    email_subject = "Activate Your Acount"

    email_body = render_to_string('activation.html', {
        'user' : user,
        'domain' : current_site.domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : generate_token.make_token(user)
    })

    email =     (subject=email_subject, body= email_body, 
                 from_email=settings.EMAIL_FROM_USER,
                 to=[user.email]
                )
    if not settings.TESTING:
        email.send()

@auth_user_should_not_access
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
            return render(request, 'register.html', context, status=409)
        
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
            return render(request, 'register.html', context, status=409)

        if context["has_error"]:
            return render(request, 'register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()
        send_verification_email(user, request)
        print("passed problem")
        messages.add_message(request, messages.SUCCESS, "Please Check the email you provided for verification")        
        return HttpResponseRedirect(reverse('users:login'))
    else:

        # initial get request new form
        #form = SignUpForm()
        return render(request, 'register.html')

@auth_user_should_not_access
def login_view(request):
    """login user"""

    if request.method != "POST":
        # intial get request
        return render(request, 'login.html')
    else:
        #context = {'data' : request.POST}
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        user = authenticate(request, username = username, password = password)
        if not user:
            # user isnt registered
            messages.add_message(request, messages.ERROR, "Invalid Credentials")
            return render(request, "login.html")
        
        if not user.email_verified:
            # email isnt verified
            messages.add_message(request, messages.ERROR, "Please Verify your email check your email inbox")
            
            return render(request, 'login.html')
   
        
        # logging in user
        login(request, user)
        
        messages.add_message(request, messages.SUCCESS, f"Welcome {user.username}")
        
        return HttpResponseRedirect(reverse('blogs:my_blogs'))


def logout_view(request):
    """logging out users"""
    logout(request)
    return HttpResponseRedirect(reverse('blogs:home'))


def activate_user(request, uid64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.email_verified = True

        user.save()

        messages.add_message(request, messages.SUCCESS, "Email Verified Successfully")

        return HttpResponseRedirect(reverse('users:login'))

    return render(request, 'activation_failed.html', {'user' : user})