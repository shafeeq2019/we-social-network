import os
import sys
import django

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()
from account.models import User

for user in User.objects.all():
    old_count = user.friends_count
    user.update_friends_count()
    if old_count != user.friends_count:
        print(f'{user.email}: {old_count} -> {user.friends_count}')
