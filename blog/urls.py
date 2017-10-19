from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.PostIndexListView.as_view(), name='index'),
    url(r'^post/(?P<slug>[\w\-]+)/$', views.PostDetailView.as_view(),
        name='detail'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.PostMonthArchiveView.as_view(month_format='%m'),
        name="archive"),
    url(r'^category/(?P<slug>[\w\-]+)/$',
        views.PostCategoryListView.as_view(), name='category'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', views.PostTagListView.as_view(),
        name='tag'),

    url(r'^post/author/(?P<slug>[\w\-]+)/$', views.PostUserListView.as_view(),
        name='post_user_list'),
    url(r'^post/(?P<slug>[\w\-]+)/edit/$', views.PostUpdate.as_view(),
        name='update_post'),
    url(r'^post/(?P<slug>[\w\-]+)/delete/$', views.PostDelete.as_view(),
        name='delete_post'),

    url(r'^action/create_post/$', views.PostCreate.as_view(),
        name='create_blog'),
    url(r'^action/create_category/$', views.CategoryCreate.as_view(),
        name='create_category'),
    url(r'^action/create_tag/$', views.TagCreate.as_view(), name='create_tag'),

]