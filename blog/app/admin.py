from django.contrib import admin
from .models import Post
from django.db import models
# Register your models here.
# admin.site.register(Post)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'author', 'created_on')
    list_filter = ('status','created_on')
    search_fields = ('title','content')


admin.site.register(Post, PostAdmin)    