import math

from django import template
from django.db.models import Count, Max, Avg, FloatField
from django.db.models.functions import TruncMonth, Lower, Cast

from ..models import Post, Category, Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(num=10):
    """ Get recent posts
    """
    return Post.objects.filter(published=True)[:num]

@register.simple_tag
def get_archives():
    """ Group posts by created month
    """
    archives = Post.objects.filter(published=True).annotate(
        date=TruncMonth('created_time')).values('date').annotate(
        num_posts=Count('id')).order_by('date')
    return archives

@register.simple_tag
def get_categories():
    """ Get all categories, ordered by name
    """
    # categories = Category.objects.filter(post__published=True).annotate(
    #     num_posts=Count('post')).order_by('-num_posts', Lower('name'))
    categories = Category.objects.filter(post__published=True).annotate(
        num_posts=Count('post')).order_by(Lower('name'))
    return categories

@register.simple_tag
def get_tags():
    """ Get all tags
    """
    max_num_posts = Tag.objects.filter(post__published=True).annotate(
        num_posts=Count('post')).aggregate(Max('num_posts')).get(
        'num_posts__max')

    if not max_num_posts:
        max_num_posts = 0

    tags = Tag.objects.filter(post__published=True).annotate(
        freq_posts=Cast(Count('post') / float(max_num_posts) * 10,
        FloatField())).filter(freq_posts__gt=0.0).order_by(Lower('name'))

    return tags