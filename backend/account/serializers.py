from .models import User, FriendshipRequest
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name',
                  'friends_count', 'posts_count', 'avatar_link']


class PrivateUserSerializer(UserSerializer):
    # Only for the logged-in user's own account
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['email']


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'status', 'created_by']
