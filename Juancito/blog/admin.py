from django.contrib import admin
from django.db import models

from martor.widgets import AdminMartorWidget

from .models import Blog

class BlogModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Blog, BlogModelAdmin)
