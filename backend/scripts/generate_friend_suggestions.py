import os
import sys
import django
import re
from collections import Counter
from django.utils import timezone
from datetime import timedelta

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()
from account.models import User
users = User.objects.all()

for user in users:
    # Clear the suggestion list
    user.people_you_may_know.clear()
    print('Find friends for:', user)
    user_friends = user.friends.all().exclude(id=user.id)
    for friend in user_friends:
        friends_of_friends = friend.friends.all().exclude(id=user.id)
        for person in friends_of_friends:
            if person not in user_friends:
                user.people_you_may_know.add(person)
        