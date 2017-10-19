from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import markdown

from .models import Post, Category, Tag
from account.decorators import group_required

class _PostListView(ListView):
    """ Paginated ListView
    """
    N_PAGE_ONESIDE = 2
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(_PostListView, self).get_context_data(**kwargs)

        # get context provided in ListView
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # get pagination data
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        """
        get custormized pagination data
        For example: page = [1, 2, 3, ..., 9], current_page = 7, NPAGE = 2
            then left = [5, 6], right = [8, 9], left_has_more = True,
            right_has_more = False, first = True, last = False
        """
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False # if ellipses is needed on the left
        right_has_more = False # if ellipses is needed on the right
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = list(paginator.page_range)

        if page_number == 1: # first page, left = [], left_has_more = False, first = False
            if 1 + self.N_PAGE_ONESIDE < len(page_range):
                right = page_range[1:1 + self.N_PAGE_ONESIDE]
            else:
                right = page_range[1:]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages: # last page, right = [], right_has_more = False, last = False
            if page_number - self.N_PAGE_ONESIDE - 1 > 0:
                left = page_range[page_number - self.N_PAGE_ONESIDE - 1:page_number - 1]
            else:
                left = page_range[:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            if page_number - self.N_PAGE_ONESIDE - 1 > 0:
                left = page_range[page_number - self.N_PAGE_ONESIDE - 1:page_number - 1]
            else:
                left = page_range[:page_number - 1]

            if page_number + self.N_PAGE_ONESIDE < len(page_range):
                right = page_range[page_number:page_number + self.N_PAGE_ONESIDE]
            else:
                right = page_range[page_number:]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class PostIndexListView(_PostListView):
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


class PostMonthArchiveView(MonthArchiveView, _PostListView):
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
            + self.MONTH_DICT[str(self.kwargs.get('month'))] \
            + ', ' + str(self.kwargs.get('year'))
        context.update({
            'title': title_string
        })
        return context


class PostCategoryListView(_PostListView):
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


class PostTagListView(_PostListView):
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


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class CategoryCreate(CreateView):
    """ View to create category
    """
    template_name = 'blog/action/create_category.html'
    success_url = '/'
    model = Category
    fields = ['name']


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class TagCreate(CreateView):
    """ View to create tag
    """
    template_name = 'blog/action/create_tag.html'
    success_url = '/'
    model = Tag
    fields = ['name']


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostCreate(CreateView):
    """ View to create post
    """
    template_name = 'blog/action/create_post.html'
    success_url = '/'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'publish' in self.request.POST:
            form.instance.published = True
        else:
            form.instance.published = False
        form.save()
        return super(PostCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostUpdate(UpdateView):
    """ View to update post
    """
    template_name = 'blog/action/update_post.html'
    success_url = '/'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        if 'publish' in self.request.POST:
            form.instance.published = True
        elif 'draft' in self.request.POST:
            form.instance.published = False
        else:
            return redirect(reverse('blog:delete_post',
                args=[self.kwargs.get('slug'),]))

        form.save()
        return super(PostUpdate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostDelete(DeleteView):
    """ View to delete post
    """
    template_name = 'blog/action/delete_post.html'
    success_url = '/'
    model = Post
    fields = ['title', 'body', 'category', 'tags']


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostUserListView(_PostListView):
    """ View to show posts by particular user for edit
    """

    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'
    model = Post

    def get_queryset(self):
        return super(PostUserListView, self).get_queryset().filter(
            author=self.request.user)