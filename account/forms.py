from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile

class UploadAvatarForm(forms.Form):
    image = forms.ImageField(label='New Avatar Image')

class DisplayNameChangeForm(forms.Form):
    display_name = forms.CharField(max_length=20, label="Name", required=False)

    def clean_display_name(self):
        display_name = self.cleaned_data['display_name']
        display_name.strip()
        if UserProfile.objects.filter(display_name=display_name).count() > 0:
            raise ValidationError('This name is already in use.')
        return display_name if display_name else None