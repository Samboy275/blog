from django.contrib import admin
from .models import Report
from blogs.models import BlogPost, Comments
# Register your models here.




@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """admin managing reports"""
    # display report porperties in a list
    list_display = ('reported_text', 'text', 'reporter', 'created_at', 'reported_id')

    def reported_text(self, report):

        return report.reported_object.text

    # filter reports based on given properties
    list_filter = ['created_at']
    # search database using
    search_fields = ('reported', 'reported_body')

    actions = ['delete_reported_item']

    def delete_reported_item(self, request, queryset):
        """delete reported items and the report"""
        for record in queryset:
            if record.report_type == 'c':
                # delete reported comment
                Comments.objects.filter(id = record.reported_id).delete()
            elif record.report_type == 'p':
                # delete reported post
                BlogPost.objects.filter(id = record.reported_id).delete()
        queryset.delete()