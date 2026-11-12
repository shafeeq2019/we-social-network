from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from account.models import User
from account.tokens import activation_token


def activate_email(request):
    uid = request.GET.get('uid', '')
    token = request.GET.get('token', '')

    try:
        user = User.objects.filter(pk=force_str(urlsafe_base64_decode(uid))).first() if uid else None
    except (ValueError, ValidationError):
        # uid is not valid base64 or not a valid UUID
        user = None

    if user and activation_token.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        return HttpResponse("<h1 style='text-align:center;'>The user is now activated. You can go ahead and log in!</h1>")
    else:
        return HttpResponse("<h1 style='text-align:center;color:red'>The activation link is invalid or has expired!</h1>", status=400)
