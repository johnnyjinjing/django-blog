from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from .models import UserProfile
from .forms import UploadAvatarForm
from account.decorators import group_required

@method_decorator(login_required, name='dispatch')
class UserProfileDetailView(DetailView):
    """ View of user profile
    """

    template_name = 'account/user_profile.html'
    context_object_name = 'user_profile'
    model = UserProfile

    def get_queryset(self):
        self.profile_user_id = get_object_or_404(UserProfile,
            slug=self.kwargs.get('slug')).user.id

        if self.request.user.id == self.profile_user_id:
            return super(UserProfileDetailView, self).get_queryset().filter(
                slug=self.kwargs.get('slug'))
        else:
            raise PermissionDenied


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user__pk=request.user.id)
            user_profile.avatar = form.cleaned_data['image']
            user_profile.save()
            return redirect(reverse('user_profile',
                args=[request.user.user_profile.slug],))
    else:
        form = UploadAvatarForm()
    return render(request, 'account/upload_avatar.html', {'form': form})