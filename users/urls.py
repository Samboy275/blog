from django.urls import path
from . import views


#urlconf for users app

app_name = 'users'

urlpatterns = [
    # login page view
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('activate_user/<uid64>/<token>', views.activate_user, name='activate')
]