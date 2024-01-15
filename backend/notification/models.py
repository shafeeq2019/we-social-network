from django.db import models
import uuid
from account.models import User
from post.models import Post


class Notification(models.Model):
    NEWFRIENDREQUEST = 'new_friendrequest'
    ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
    REJECTEDFRIENDREQUEST = 'rejected_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friendrequest'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
        (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment'),
        (POST_COMMENT, 'Post comment')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    post_id = models.ForeignKey(
        Post, related_name='notifications', on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(
        max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    created_by = models.ForeignKey(
        User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(
        User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
