from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import User


def clean_unique_email(form):
    # Emails are case-insensitive: store them lowercase and reject
    # addresses that only differ in case from an existing one
    email = form.cleaned_data['email'].lower()
    users = User.objects.filter(email__iexact=email)
    if form.instance.pk:
        users = users.exclude(pk=form.instance.pk)
    if users.exists():
        raise ValidationError('User with this Email already exists.', code='unique')
    return email


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')

    def clean_email(self):
        return clean_unique_email(self)


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'avatar')

    def clean_email(self):
        return clean_unique_email(self)
