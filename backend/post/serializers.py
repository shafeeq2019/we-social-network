from .models import Post
from rest_framework import serializers
from account.serializers import UserSerializer
from django.utils.timesince import timesince
from datetime import datetime, timezone



# class PostSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     created_at_ago = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id', 'body', 'created_by', 'created_at', 'created_at_ago']

#     def get_created_at_ago(self, obj):
#         now = datetime.now(timezone.utc)  # Make sure it's also aware
#         return timesince(obj.created_at, now)


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_by', 'created_at', 'created_ago']


