from blog.models import Blog

from django.views.generic import ListView

class Blogposts(ListView):
    queryset = Blog.objects.order_by('-publication_date')
    template_name = "index.html"
    paginate_by = 5
    context_object_name = 'blog_list'
