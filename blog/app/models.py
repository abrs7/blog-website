from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

STATUS = ((0,'Draft'),(1,'Published'))
class Post(models.Model):
    title = models.CharField(max_length =256, unique=True)
    slug = models.SlugField(max_length=256, unique=True )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    content = models.TextField()
    status = models.IntegerField(choices = STATUS, default= 0)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


    class Meta():
        ordering = ['-created_on']

    def __str__(self):
        return self.title    
