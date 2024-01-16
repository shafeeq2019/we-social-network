from django.http import HttpResponse
from django.shortcuts import render

from account.models import User

# Create your views here.


def activate_email(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(id=id, email=email)
        if user:
            user.is_active = True
            user.save()
            return HttpResponse("<h1 style='text-align:center;'>The user is now activated. You can go ahead and log in!</h1>")
    else:
        return HttpResponse("<h1 style='text-align:center;color:red'>The parameters are not valid!</h1>")
