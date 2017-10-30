from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'blog'

urlpatterns = [

    # display views
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
    url(r'^author/(?P<slug>[\w\-]+)/$', views.PostAuthorListView.as_view(),
        name='author'),

    # post backend views
    url(r'^myposts/$', views.PostUserListView.as_view(),
        name='post_user_list'),
    url(r'^action/post_create/$', views.PostCreate.as_view(),
        name='post_create'),
    url(r'^post/(?P<slug>[\w\-]+)/edit/$', views.PostUpdate.as_view(),
        name='post_update'),
    url(r'^post/(?P<slug>[\w\-]+)/delete/$', views.PostDelete.as_view(),
        name='post_delete'),


    # other backend
    url(r'^action/category_create/$', views.CategoryCreate.as_view(),
        name='category_create'),
    url(r'^action/tag_create/$', views.TagCreate.as_view(), name='tag_create'),

    # search
    url(r'^search/', views.CustomSearchView.as_view(),
        name='search'),

    # contact
    url(r'^contact/$', views.ContactFormView.as_view(),
        name='contact'),
    url(r'^contact/thanks/$',
        TemplateView.as_view(template_name="blog/thanks.html"),
        name='thanks'),
]