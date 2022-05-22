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

	created_at = models.DateTimeField(auto_now_add=True)
	reporter = models.ForeignKey(User, related_name='reporter')
	report_type = models.String(choices = REPORT_TYPES, max_length= 1) 