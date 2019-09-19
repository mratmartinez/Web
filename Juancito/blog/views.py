import os, json

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify
from martor.utils import LazyEncoder
from blog.models import Blog

from django.views.generic import DetailView, ListView

class Blogposts(ListView):
    queryset = Blog.objects.order_by('-post_date')
    template_name = 'index.html'
    paginate_by = 5
    context_object_name = 'blog_list'

class Post(DetailView):
    template_name = 'post.html'
    model = Blog
    context_object_name = 'post'

@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            name = image.name.split('.')
            extension = name[-1]
            if len(name) > 2:
                img_slug = slugify('-'.join(name[0:-1]))
            else:
                img_slug = slugify(name[0])
            filename = img_slug + '.' + extension
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, filename)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.IMAGES_URL, filename)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': filename
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))
