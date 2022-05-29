from blogs.models import BlogPost
from blogs.models import Comments
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from report.models import Report




# signals that handle deletion of comments and posts to delete their reports


@receiver(pre_delete, sender=BlogPost)
@receiver(pre_delete, sender=Comments)
def delete_post_report(sender, instance, using, **kwargs):

	report_t = ''
	if sender.__name__ == 'BlogPost':
		report_t = 'p'
	elif sender.__name__ == 'Comments':
		report_t = 'c'

	report = Report.objects.filter(reported_id = instance.id, report_type=report_t)

	if len(report) > 0:
		print("found report")
		report.all().delete()