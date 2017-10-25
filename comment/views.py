from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .models import Comment
from .forms import CommentForm
from blog.models import Post

@login_required
def comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = User.objects.get(username=request.user.username)
            comment.save()
            return redirect(post)

        else:
            return redirect(post)
    return redirect(post)