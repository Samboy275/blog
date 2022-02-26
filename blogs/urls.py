
from unicodedata import name
from django.views import View
from django.urls import path, URLPattern
from . import views

app_name = 'blogs'
urlpatterns = [
    # homepage
    path('', views.home, name='home'),
    # add a new post
    path('new_post', views.new_blog, name='new_post'),
    # edit post
    path('edit_post/<blog_id>', views.edit_post, name='edit_post'),
    # view user blogs
    path('my_blogs/<user_id>', views.my_blogs_view, name='my_blogs'),
    # view one post
    path('my_post/<post_id>', views.post_view, name='my_post'),
]