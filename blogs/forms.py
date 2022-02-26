from pydoc_data.topics import topics
from django import forms
from .models import BlogPost, Comments


class BlogPostForm(forms.ModelForm):
    """form for adding new posts"""
    class Meta:
        model = BlogPost
        fields = ['title' ,'text', 'public']
        labels = { 'title': '' ,'text' : ''}
        widgets = {'text' : forms.Textarea(attrs={'cols': 80})}

class Comments_Form(forms.ModelForm):
    """forms for comments"""

    class Meta:
        model = Comments
        fields = ['text']
        widegts = {'text' : forms.Textarea(attrs={'rows' : 15 ,'cols' : 15})}