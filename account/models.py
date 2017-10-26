import os

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.template.defaultfilters import slugify

from registration.signals import user_activated

from .utils import OverwriteStorage, UploadToPathAndRename
from .utils import create_avatar

class UserProfile(models.Model):
    """ User Profile model, one-to-one relation with User
    user: User model instance
    avatar: user avatar
    """

    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name='user_profile')

    # Additional attributes
    avatar = models.ImageField(
        upload_to=UploadToPathAndRename(settings.AVATAR_DIR),
        storage=OverwriteStorage(), null=True,blank=True)

    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
        if self.avatar:
            fname = create_avatar(self.avatar.path)
            self.avatar = os.path.join(settings.AVATAR_DIR, fname)
        super(UserProfile, self).save(*args, **kwargs)



@receiver(user_activated)
def post_user_activation(sender, user, request, **kwargs):
    """ Create UserProfile model and assign user to the default group
    called when the user activate the account
    """
    group = Group.objects.get(name=settings.DEFAULT_GROUP_NAME)
    group.user_set.add(user)
    profile = UserProfile(user=user)
    profile.save()




