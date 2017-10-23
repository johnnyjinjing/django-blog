from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    parent = forms.ModelChoiceField(queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Write a comment"

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return Comment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the parent field field
        data = super(CommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data

    class Meta:
        model = Comment
        fields = ['body', 'parent']