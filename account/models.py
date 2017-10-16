from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from registration.signals import user_activated

class UserProfile(models.Model):
    """ User Profile model, one-to-one relation with User
    user: User model instance
    avatar: user avatar
    """

    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Additional attributes
    avatar = models.ImageField(upload_to='profile_avatars', null=True,
        blank=True)

@receiver(user_activated)
def create_user_profile(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()