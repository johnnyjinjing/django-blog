from django.shortcuts import render
from django.views.generic import DetailView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UploadAvatarForm

class UserProfileDetailView(DetailView):
    """ View of user profile
    """

    template_name = 'account/user_profile.html'
    context_object_name = 'user_profile'
    model = UserProfile

    def get_queryset(self):
        if self.request.user.id == int(self.kwargs.get('pk')):
            return super(UserProfileDetailView, self).get_queryset().filter(
                user__pk=self.kwargs.get('pk'))
        else:
            raise Http404("Permission denied!")

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user__pk=request.user.id)

            # user_profile.avatar = form.cleaned_data['image']
            user_profile.avatar = _create_thumbnail(form.cleaned_data['image'])
            user_profile.save()
            # return HttpResponseRedirect('/')
            return HttpResponse('image upload success')
    else:
        form = UploadAvatarForm()
    return render(request, 'account/upload_avatar.html', {'form': form})