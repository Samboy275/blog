from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseServerError, JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comments
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
    comments = post.comments.all()
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
def delete_post(request):
    """Deleting a post"""
    
    # delete confirmation
    if request.method == "POST":
        post_id = request.POST.get("id")
        print(post_id)
        post = get_object_or_404(BlogPost, pk=post_id)
        print(post)
        post.delete()

        messages.add_message(request, messages.SUCCESS, "Deleted Post")
        return JsonResponse({
            "message" : "deleted post"
        })

    post_id = request.GET.get("id")
    post = get_object_or_404(BlogPost, pk=post_id)
    context = {"post" : post}
    template = render_to_string("delete_post.html", context)
    return JsonResponse({"form" : template})


def delete_comment(request):
    """ deleting a comment"""

    

    if request.method == "POST":
        
        comment_id = request.POST.get("id")
        comment = get_object_or_404(Comments, pk=comment_id)
        comment.delete()
        return JsonResponse({
            'message' : 'Deleted comment'
        })
# 505 error handler
def server_error(request):
    
    return HttpResponseServerError(request, '500.html')