from re import template
from unicodedata import name
from django.urls import URLPattern, path
from django.contrib.auth.views import LoginView
from . import views


#urlconf for users app

app_name = 'users'

urlpatterns = [
    # login page view
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register')
]