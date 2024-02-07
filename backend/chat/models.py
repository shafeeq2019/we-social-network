from django.db import models
import uuid
from account.models import User
from django.utils.timesince import timesince


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations_in')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name=("conversations"), on_delete=models.CASCADE)

    def modified_ago(self):
        return timesince(self.modified_at)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, related_name=("messages"), on_delete=models.CASCADE)
    message = models.TextField()
    sent_to = models.ForeignKey(User,  related_name=(
        "received_messages"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,  related_name=(
        "sent_messages"), on_delete=models.CASCADE)

    def created_ago(self):
        return timesince(self.created_at)
