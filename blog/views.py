from .models import Post
from django.views.generic import ListView

class PostIndexListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    model = Post

    def get_queryset(self):
        return super(PostIndexListView, self).get_queryset().filter(
            published=True)