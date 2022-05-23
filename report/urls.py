from typing import ValuesView
from django.urls import path
from . import views



# url conf for reports

app_name = 'report'


urlpatterns = [
    path('new-report', views.report_view, name="new_report"),
]