from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from blog.models import Post
from .models import Comment
from .forms import CommentForm
from account.decorators import group_required

@login_required
@group_required('reader')
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
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)