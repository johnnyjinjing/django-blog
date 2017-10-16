from django import forms

class UploadAvatarForm(forms.Form):
    image = forms.ImageField()