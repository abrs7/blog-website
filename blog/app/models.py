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

##user comment Model
class Comment(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments', max_length= 256)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Comment from {self.name.username} with post {self.post}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length = 256, blank = False)
    last_name = models.CharField(max_length = 256, blank = False)
    profile_pic = models.ImageField()
    bio = models.TextField()
    linkedin_url = models.URLField(max_length = 105)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)



    


