from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
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
        upload_to=UploadToPathAndRename('profile_avatars'),
        storage=OverwriteStorage(), null=True,blank=True)

    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
        if self.avatar:
            create_avatar(self.avatar.path)


@receiver(user_activated)
def create_user_profile(sender, user, request, **kwargs):
    """ Create UserProfile model, called when the user activate the account
    """
    profile = UserProfile(user=user)
    profile.save()


