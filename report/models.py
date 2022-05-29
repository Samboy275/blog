from django.db import models
from users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Report(models.Model):
	POST = 'p'
	COMMENT = 'c'

	REPORT_TYPES = (
		(POST, 'post'),
		(COMMENT, 'comment')
	)
	text = models.CharField(max_length=250, default='')
	created_at = models.DateTimeField(auto_now_add=True)
	reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.CASCADE)
	report_type = models.CharField(choices = REPORT_TYPES, max_length= 1)
	reported_id = models.PositiveIntegerField()
	reported_body = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	reported_object = GenericForeignKey('reported_body', 'reported_id')
	

	class Meta:
		indexes = [
			models.Index(fields = ['reported_body', 'reported_id'])
		]



