from .models import Notification
from rest_framework import serializers
from account.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'body', 'type_of_notification', 'created_by','created_for_id', 'post_id']
