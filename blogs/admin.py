from django.contrib import admin
from .models import BlogPost, Comments
# Register your models here.

admin.site.register(BlogPost)

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    """ admin managing comments """
    #displays properties specified for each comment in alist
    list_display = ('post','text' , 'owner', 'date_added')
    # filter comments based on given properties
    list_filter = ('date_added',)
    # search database using givein properties 
    search_fields = ('post', 'text', 'owner')
    # uses approve action method to update active field for a set of comments

