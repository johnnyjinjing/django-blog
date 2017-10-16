from django.conf.urls import url

from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView

from . import views

urlpatterns = [
    # user profile
    url(r'^profile/(?P<pk>[0-9]+)/$',
        login_required(views.UserProfileDetailView.as_view()), name='user_profile'),

    # upload avatar
    url(r'^profile/upload_avatar/$', views.upload_avatar, name='upload_avatar'),

    # use unique email form
    url(r'^register/$',
        RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),
    # use HTML email
    url(r'^password/reset/$',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('auth_password_reset_done'),
            html_email_template_name='registration/password_reset_email.html'
        ), name='auth_password_reset'),
]