from hashlib import new
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseServerError
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm, Comments_Form
# Create your views here.

def home(request):
    """display home page"""
    blogs = BlogPost.objects.filter(public = True).order_by("date_added")
    context = {'blogs': blogs}

    return render(request, 'home.html', context)

@login_required
def new_blog(request):
    """add a new blog"""

    if request.method != "POST":
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            messages.add_message(request, messages.SUCCESS, "Blog Added successfully")
            return HttpResponseRedirect(reverse('blogs:my_blogs'))
    context = {'form' : form}
    return render(request, 'new_post.html', context)

@login_required
def edit_post(request, blog_id):
    """edit an exsiting blog"""

    post = BlogPost.objects.get(id=blog_id)
    name = post.title
    # check is request user is owner
    if request.user != post.owner:
        raise Http404
    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Blog editted successfully")
            return HttpResponseRedirect(reverse('blogs:my_post', args=[blog_id]))
    context = {'blog' : post, 'form' : form, 'name' : name }

    return render(request, 'edit_post.html', context)


@login_required
def my_blogs_view(request):
    """displays blogs of the user"""
    posts = BlogPost.objects.filter(owner = request.user)

    context = {'posts' : posts}

    return render(request, 'my_blogs.html', context)

def post_view(request, post_id):
    """displays a single post"""

    post = BlogPost.objects.get(id = post_id)
    #comments 
    comments = post.comments.filter(active=True)
    comment_form = None
    new_comment = None
    if request.user.is_authenticated:
            # handling comments for each post
            if request.method == 'POST':
                comment_form = Comments_Form(data=request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.post = post
                    new_comment.owner = request.user
                    new_comment.save()
            else:
                comment_form = Comments_Form()

    context = {'post': post, 'comments' : comments, 'new_comment' : new_comment, 'comment_form' : comment_form}
    return render(request, 'blog.html', context)

@login_required
def delete_post(request, post_id):
    """Deleting a post"""
    post = get_object_or_404(BlogPost, pk=post_id)
    # delete confirmation
    if request.method == "POST":
        post.delete()

        messages.add_message(request, messages.SUCCESS, "Deleted Post")
        return HttpResponseRedirect(reverse('blogs:my_blogs'))

    
    context = {"post" : post}
    return render(request, "delete_post.html", context)

# 505 error handler
def server_error(request):
    
    return HttpResponseServerError(request, '500.html')