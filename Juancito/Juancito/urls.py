from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static

import martor

from blog.views import Blogposts, Post, markdown_uploader

urlpatterns = [
    path('', Blogposts.as_view()),
    path('api/uploader/', markdown_uploader, name='markdown_uploader_page'),
    path('<str:slug>', Post.as_view()),
    path('martor/', include('martor.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
