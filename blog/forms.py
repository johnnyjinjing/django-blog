from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label='Name')
    contact_email = forms.EmailField(required=True, label='Email')
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label='Message'
    )

    def send_email(self, request=None):
        email = EmailMessage(
            subject="New message from " + self.cleaned_data['contact_name'] \
                + " on " + get_current_site(request).name,
            body=self.cleaned_data['content'],
            to=[settings.CONTACT_EMAIL_RECIPIENT,],
            headers = {'Reply-To': self.cleaned_data['contact_email']}
        )
        email.send()