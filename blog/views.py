from django.views.generic import ListView, DetailView

import markdown

from .models import Post

class PostIndexListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    model = Post

    def get_queryset(self):
        return super(PostIndexListView, self).get_queryset().filter(
            published=True)

class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    model = Post

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object()
        post.body = markdown.markdown(post.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
        return post

    def get_queryset(self):
        return super(PostDetailView, self).get_queryset().filter(
            published=True)