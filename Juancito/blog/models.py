from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from taggit.managers import TaggableManager

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    post_date = models.DateField(default=date.today)
    updated = models.DateField(auto_now = True)
    text = models.TextField(max_length=10600)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
