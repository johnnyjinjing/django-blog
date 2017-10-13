from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.PostIndexListView.as_view(), name='index'),
    url(r'^post/(?P<slug>[\w\-]+)/$', views.PostDetailView.as_view(),
        name='detail'),
]