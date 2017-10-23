from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import markdown

from .models import Post, Category, Tag
from account.decorators import group_required
from .base_views import PaginatedListView, MiscCreateMixin
from comment.forms import CommentForm


class PostIndexListView(PaginatedListView):
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

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class PostMonthArchiveView(MonthArchiveView, PaginatedListView):
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


class PostCategoryListView(PaginatedListView):
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
        context = super(PaginatedListView, self).get_context_data(**kwargs)
        title_string = 'Posts in Category: ' + self.cat.name
        context.update({
            'title': title_string
        })
        return context


class PostTagListView(PaginatedListView):
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
        context = super(PaginatedListView, self).get_context_data(**kwargs)
        title_string = 'Posts with Tag: ' + self.tag.name
        context.update({
            'title': title_string
        })
        return context


class CategoryCreate(MiscCreateMixin):
    """ View to create category
    """
    template_name = 'blog/action/create_category.html'
    model = Category
    fields = ['name']

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        else:
            return reverse('blog:index')


class TagCreate(MiscCreateMixin):
    """ View to create tag
    """
    template_name = 'blog/action/create_tag.html'
    model = Tag
    fields = ['name']

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        else:
            return reverse('blog:index')


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostCreate(CreateView):
    """ View to create post
    """
    template_name = 'blog/action/create_post.html'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'publish' in self.request.POST:
            form.instance.published = True
        elif 'draft' in self.request.POST:
            form.instance.published = False
        elif "discard" in self.request.POST:
            return redirect(reverse('blog:post_user_list',
                args=[self.request.user.user_profile.slug,]))

        form.save()
        return super(PostCreate, self).form_valid(form)

    def form_invalid(self, form):
        if "discard" in self.request.POST:
            return redirect(reverse('blog:post_user_list',
                args=[self.request.user.user_profile.slug,]))
        return super(PostCreate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('blog:post_user_list',
        args=[self.request.user.user_profile.slug,])


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostUpdate(UpdateView):
    """ View to update post
    """
    template_name = 'blog/action/update_post.html'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        if 'publish' in self.request.POST:
            form.instance.published = True
        elif 'draft' in self.request.POST:
            form.instance.published = False
        elif "delete" in self.request.POST:
            return redirect(reverse('blog:delete_post',
                args=[self.kwargs.get('slug'),]))

        form.save()
        return super(PostUpdate, self).form_valid(form)

    def form_invalid(self, form):
        if "delete" in self.request.POST:
            return redirect(reverse('blog:delete_post',
                args=[self.kwargs.get('slug'),]))
        return super(PostUpdate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('blog:post_user_list',
        args=[self.request.user.user_profile.slug,])


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostDelete(DeleteView):
    """ View to delete post
    """
    template_name = 'blog/action/delete_post.html'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def get_success_url(self):
        return reverse('blog:post_user_list',
        args=[self.request.user.user_profile.slug,])


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostUserListView(PaginatedListView):
    """ View to show posts by particular user for edit
    """

    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'
    model = Post

    def get_queryset(self):
        return super(PostUserListView, self).get_queryset().filter(
            author=self.request.user)