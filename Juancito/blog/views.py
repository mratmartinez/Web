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
