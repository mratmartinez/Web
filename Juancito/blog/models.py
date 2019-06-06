import os
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from taggit.managers import TaggableManager
from martor.models import MartorField

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=170)
    slug = models.SlugField(max_length=170, unique=True, null=True, blank=True)
    post_date = models.DateField(default=date.today)
    updated = models.DateField(auto_now = True)
    text = MartorField(max_length=10600)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
