from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import UploadAvatarForm

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
            raise Http404("Permission denied!")

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user__pk=request.user.id)

            user_profile.avatar = form.cleaned_data['image']

            # user_profile.avatar = create_avartar(form.cleaned_data['image'])
            user_profile.save()
            # return HttpResponseRedirect('/')
            return HttpResponse('image upload success')
    else:
        form = UploadAvatarForm()
    return render(request, 'account/upload_avatar.html', {'form': form})