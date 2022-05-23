
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
        lablels = {'text' : 'comment'}
        widegts = {'text' : forms.Textarea(attrs={'rows' : 4 ,'cols' : 15})}