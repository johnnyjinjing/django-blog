from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.PostIndexListView.as_view(), name='index'),
    url(r'^post/(?P<slug>[\w\-]+)/$', views.PostDetailView.as_view(),
        name='detail'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.PostMonthArchiveView.as_view(month_format='%m'), name="archive"),
    url(r'^category/(?P<slug>[\w\-]+)/$', views.PostCategoryListView.as_view(),
        name='category'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', views.PostTagListView.as_view(),
        name='tag'),

    url(r'^action/create_post/$', login_required(views.PostCreate.as_view()),
        name='create_blog'),
    url(r'^action/create_category/$',
        login_required(views.CategoryCreate.as_view()), name='create_category'),
    url(r'^action/create_tag/$', login_required(views.TagCreate.as_view()),
        name='create_tag'),
]