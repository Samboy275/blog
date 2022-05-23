from django import forms
from .models import Report




class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['text']
        labels = {'text' : 'report reason'}
        widegets = { 'text' : forms.Textarea(attrs={'rows' : 2, 'cols' : 10})} 