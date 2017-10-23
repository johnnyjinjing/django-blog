from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<post_slug>[\w\-]+)/add/$', views.comment, name='comment'),
]