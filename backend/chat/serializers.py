from .models import Conversation, ConversationMessage
from rest_framework import serializers
from account.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'modified_ago']


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ['id', 'message', 'sent_to',
                  'created_at', 'created_by', 'created_ago']


class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'modified_ago', 'messages']
