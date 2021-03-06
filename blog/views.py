from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

import markdown
from markdown.extensions.toc import TocExtension
from haystack.generic_views import SearchView

from .base_views import PaginatedMixin, MiscCreateMixin, PaginatedListView
from .models import Post, Category, Tag
from .forms import ContactForm
from account.decorators import group_required
from account.models import UserProfile
from comment.forms import CommentForm


# Post List views
class PostIndexListView(PaginatedListView):
    """ View of Blog index page
    """

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    model = Post

    def get_queryset(self):
        return super(PostIndexListView, self).get_queryset().filter(
            published=True)


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
        context = super(PostMonthArchiveView, self).get_context_data(**kwargs)
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
        context = super(PostCategoryListView, self).get_context_data(**kwargs)
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
        context = super(PostTagListView, self).get_context_data(**kwargs)
        title_string = 'Posts with Tag: ' + self.tag.name
        context.update({
            'title': title_string
        })
        return context


class PostAuthorListView(PaginatedListView):
    """ View of author page
    """

    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    allow_empty = False # raise 404 error if there are no posts
    model = Post

    def get_queryset(self):
        self.author = get_object_or_404(UserProfile,
            slug=self.kwargs.get('slug')).user
        return super(PostAuthorListView, self).get_queryset().filter(
            author=self.author, published=True)

    def get_context_data(self, **kwargs):
        context = super(PostAuthorListView, self).get_context_data(**kwargs)
        if self.author.user_profile.display_name:
            title_string = 'Posts by Author: ' \
                + self.author.user_profile.display_name
        else:
            title_string = 'Posts by Author: ' + self.author.username
        context.update({
            'title': title_string
        })
        return context


# Post detail views
class PostDetailView(DetailView):
    """ View of single blog page
    """

    template_name = 'blog/detail.html'
    context_object_name = 'post'
    model = Post

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object()

        # markdown support
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])

        post.body = md.convert(post.body)

        # default is: <div class="toc"><ul></ul></div>, which length is 35
        if len(md.toc) > 35:
            post.toc = md.toc

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


# Post backend
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


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostCreate(CreateView):
    """ View to create post
    """
    template_name = 'blog/action/post_create.html'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'publish' in self.request.POST:
            form.instance.published = True
            form.save()
        elif 'draft' in self.request.POST:
            form.instance.published = False
            form.save()
        elif "discard" in self.request.POST:
            return redirect(reverse('blog:post_user_list'))
        elif 'preview' in self.request.POST:
            post = form.save(commit=False)
            post.created_time = timezone.now()
            post.id = 1

            # markdown
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            post.body = md.convert(post.body)
            if len(md.toc) > 35:
                post.toc = md.toc

            context = {
                'post': post,
                'tags': form.cleaned_data['tags'],
                'title': 'Preview:',
            }
            return render(self.request, 'blog/detail_preview.html',
                context=context)

        return super(PostCreate, self).form_valid(form)

    def form_invalid(self, form):
        if "discard" in self.request.POST:
            return redirect(reverse('blog:post_user_list'))
        return super(PostCreate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('blog:post_user_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostUpdate(UpdateView):
    """ View to update post
    """
    template_name = 'blog/action/post_update.html'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        if 'publish' in self.request.POST:
            form.instance.published = True
            form.save()
        elif 'draft' in self.request.POST:
            form.instance.published = False
            form.save()
        elif 'delete' in self.request.POST:
            return redirect(reverse('blog:post_delete',
                args=[self.kwargs.get('slug'),]))
        elif 'preview' in self.request.POST:
            post = form.save(commit=False)

            # markdown
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            post.body = md.convert(post.body)
            if len(md.toc) > 35:
                post.toc = md.toc

            comment_list = self.object.comment_set.all()
            context = {
                'post': post,
                'tags': form.cleaned_data['tags'],
                'title': 'Preview:',
            }
            return render(self.request, "blog/detail_preview.html",
                context=context)

        return super(PostUpdate, self).form_valid(form)

    def form_invalid(self, form):
        if "delete" in self.request.POST:
            return redirect(reverse('blog:post_delete',
                args=[self.kwargs.get('slug'),]))
        return super(PostUpdate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('blog:post_user_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class PostDelete(DeleteView):
    """ View to delete post
    """
    template_name = 'blog/action/post_delete.html'
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def get_success_url(self):
        return reverse('blog:post_user_list')


# Other backend
@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class CategoryCreate(MiscCreateMixin):
    """ View to create category
    """
    template_name = 'blog/action/category_create.html'
    model = Category
    fields = ['name']

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        else:
            return reverse('blog:index')


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required(True, 'writer'),
    name='dispatch')
class TagCreate(MiscCreateMixin):
    """ View to create tag
    """
    template_name = 'blog/action/tag_create.html'
    model = Tag
    fields = ['name']

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        else:
            return reverse('blog:index')


# Search view
class CustomSearchView(PaginatedMixin, SearchView):
    """ Customized SearchView, disable haystack default pagination
    """

    def get_context_data(self, *args, **kwargs):
        context = super(CustomSearchView, self).get_context_data(*args,
            **kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

# Contact View
class ContactFormView(FormView):
    """ Contact View
    """
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:thanks')

    def form_valid(self, form):
        form.send_email()
        return super(ContactFormView, self).form_valid(form)