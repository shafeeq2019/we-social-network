from django import forms
from django.forms import ModelForm

from backend.validators import IMAGE_VALIDATORS
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body','created_by','is_private')


class PostAttachmentForm(forms.Form):
    image = forms.ImageField(validators=IMAGE_VALIDATORS)
