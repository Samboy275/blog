from django.db import models
from users.models import User



# Create your models here.
class Report(models.Model):
	POST = 'p'
	COMMENT = 'c'

	REPORT_TYPES = (
		(POST, 'post'),
		(COMMENT, 'comment')
	)
	# TODO : need to fix the model so it can store a refrence to the reported item
	
	text = models.CharField(max_length=250, default='')
	created_at = models.DateTimeField(auto_now_add=True)
	reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.CASCADE)
	report_type = models.CharField(choices = REPORT_TYPES, max_length= 1)
	reported_id = models.IntegerField(null=False, blank=False, default="6")
	reported_body = models.TextField(null=False, blank=False, default="")




