from django.db import models
import uuid
from post.models import Post
from account.models import User


class NotificationManager(models.Manager):
    def create_notification(self, **kwargs):
        body = self.get_body_from_type(
            kwargs['type_of_notification'], kwargs['created_by'])
        kwargs['body'] = body

        checkIfAlreadyExist = self.filter(**kwargs, is_read=False)

        if kwargs['created_by'] != kwargs['created_for'] and not checkIfAlreadyExist:
            return self.create(**kwargs)

    def get_body_from_type(self, type_of_notification, created_by):
        if type_of_notification == 'post_like':
            return f'{created_by.name} liked one of your posts!'
        elif type_of_notification == 'post_comment':
            return f'{created_by.name} commented on one of your posts!'
        elif type_of_notification == 'new_friendrequest':
            return f'{created_by.name} sent you a friend request!'
        elif type_of_notification == 'accepted_friendrequest':
            return f'{created_by.name} accepted your friend request!'
        elif type_of_notification == 'rejected_friendrequest':
            return f'{created_by.name} rejected your friend request!'


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
    post = models.ForeignKey(
        Post, related_name='notifications', on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(
        max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    created_by = models.ForeignKey(
        User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(
        User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = NotificationManager()
