from django import forms

class UploadAvatarForm(forms.Form):
    image = forms.ImageField(label='New Avatar Image')