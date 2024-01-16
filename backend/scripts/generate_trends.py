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
from post.models import Post,Trend

hashtag_pattern = re.compile(r'\B#\w+')
trends = []
posts = Post.objects.filter(body__contains='#', created_at__gte=timezone.now() - timedelta(hours=24))
for post in posts:
    hashtags_matches = hashtag_pattern.findall(post.body)
    for hashtag in hashtags_matches:
        trends.append(hashtag.lower()[1:])
        
# delete all the trends in the db
for trend in Trend.objects.all():
    trend.delete()

for trend in Counter(trends).most_common(10):
    Trend.objects.create(hashtag=trend[0], occurences=trend[1])