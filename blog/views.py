from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.dates import MonthArchiveView

import markdown

from .models import Post, Category, Tag

class PostIndexListView(ListView):
    """ View of Blog index page
    """

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    model = Post

    def get_queryset(self):
        return super(PostIndexListView, self).get_queryset().filter(
            published=True)


class PostDetailView(DetailView):
    """ View of single blog page
    """

    template_name = 'blog/detail.html'
    context_object_name = 'post'
    model = Post

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object()

        # markdown support
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


class PostMonthArchiveView(MonthArchiveView):
    """ View of Monthly Archive page
    """

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    date_field = 'created_time' # archive by this field
    allow_empty = False # raise 404 error if there are no posts
    model = Post

    MONTH_DICT = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May',
        '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov',
        '12':'Dec'}

    def get_queryset(self):
        return super(PostMonthArchiveView, self).get_queryset().filter(
            published=True)

    def get_context_data(self, **kwargs):
        context = super(MonthArchiveView, self).get_context_data(**kwargs)
        title_string = 'Posts published in: ' \
            + PostMonthArchiveView.MONTH_DICT[str(self.kwargs.get('month'))] \
            + ', ' + str(self.kwargs.get('year'))
        context.update({
            'title': title_string
        })
        return context


class PostCategoryListView(ListView):
    """ View of categoty page
    """

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    allow_empty = False # raise 404 error if there are no posts
    model = Post

    def get_queryset(self):
        self.cat = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return super(PostCategoryListView, self).get_queryset().filter(
            category=self.cat, published=True)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title_string = 'Posts in Category: ' + self.cat.name
        context.update({
            'title': title_string
        })
        return context

class PostTagListView(ListView):
    """ View of tag page
    """

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    allow_empty = False # raise 404 error if there are no posts
    model = Post

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return super(PostTagListView, self).get_queryset().filter(
            tags=self.tag, published=True)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title_string = 'Posts with Tag: ' + self.tag.name
        context.update({
            'title': title_string
        })
        return context