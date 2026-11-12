from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlencode, urlsafe_base64_encode


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    # Signed with SECRET_KEY and valid for PASSWORD_RESET_TIMEOUT (3 days).
    # is_active is part of the hash, so a link stops working once it was used.
    key_salt = 'account.tokens.ActivationTokenGenerator'

    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.is_active}{user.email}{timestamp}'


activation_token = ActivationTokenGenerator()


def build_activation_url(user):
    params = urlencode({
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
    })
    return f'{settings.WEBSITE_URL}/activateemail/?{params}'
