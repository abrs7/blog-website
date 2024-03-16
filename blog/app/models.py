from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator
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
    OCCUPATION_CHOICES = [
        ('Web Development', 'Web Development'),
        ('App Development', 'App Development'),
        ('Software Engineering', 'Software Engineering'),
        ('ML Engineer', 'ML Engineer'),
        ('Ethical Hacker', 'Ethical Hacker'),
        ('Blockchain', 'Blockchain'),
        ('Cryptography', 'Cryptography'),
    ]
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256, blank=False)
    profile_pic = models.ImageField(null=True, blank=True,default='images/bg.jpg', upload_to='images/')
    bio = models.TextField()
    linkedin_url = models.URLField(max_length=105, default='')
    location = models.CharField(max_length=30, default='', blank=True)
    birth_date = models.DateField(null=True, default='', blank=True)
    phone = models.IntegerField(null=True,default='', blank=True)  # Allow null values
    github = models.URLField(max_length=256, default='')
    occupation = models.CharField(max_length=256,default='', choices=OCCUPATION_CHOICES)
    website_url = models.URLField(max_length=256, default='')
    instagram_url = models.URLField(max_length=256, default='')
    facebook_url = models.URLField(max_length=256, default='')  # Provide a default value
    twitter_url = models.URLField(max_length=256, default='')
    programming_proficiency = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    problem_solving = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    critical_thinking = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    communication_skills = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    adaptability = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    attention_to_detail = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return str(self.user)
   

    


