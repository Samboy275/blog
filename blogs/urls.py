from django.urls import path
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
    path('my_blogs/', views.my_blogs_view, name='my_blogs'),
    # view one post
    path('my_post/<post_id>', views.post_view, name='my_post'),
    # delete a post
    path('delete_post/<post_id>', views.delete_post, name='delete_post'),
    path('delete_comment', views.delete_comment, name='delete_comment'),
]