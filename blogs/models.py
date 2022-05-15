from email.policy import default
from pyexpat import model
from django.db import models
from users.models import User
# Create your models here.


class BlogPost(models.Model):
    """blogs"""

    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added  = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text
    


class Comments(models.Model):
    """comments for a blog"""

    # related name will allow us to retireive post comments using post.comments.all()
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        # orders comments in a list by date
        ordering = ['-date_added']
    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + ' ....'
        else:
            return self.text