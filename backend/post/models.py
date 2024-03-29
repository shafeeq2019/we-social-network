from django.db import models
import uuid
from account.models import User
from django.conf import settings
from django.utils.timesince import timesince

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def created_ago(self):
        return timesince(self.created_at)

    def add_like(self, user):
        user_has_liked = self.likes.filter(created_by=user).exists()
        if user_has_liked:
            like_to_delete = Like.objects.get(post=self, created_by=user)
            like_to_delete.delete()
            self.likes_count -= 1
            self.save()
            return "post disliked successfully"

        else:
            Like.objects.create(post=self, created_by=user)
            self.likes_count += 1
            self.save()
            self.notifications.create_notification(
                created_by=user, created_for=self.created_by, type_of_notification='post_like')
            return "post liked successfully"

    def add_comment(self, user, comment):
        Comment.objects.create(created_by=user, post=self, comment=comment)
        self.comments_count += 1
        self.save()
        self.notifications.create_notification(
            created_by=user, created_for=self.created_by, type_of_notification='post_comment')
        return 'post commented successfully'
    
    def delete_comment(self, user, comment_id):
        comment = Comment.objects.filter(id=comment_id, created_by=user)
        if comment.exists():
            comment[0].delete()
            self.comments_count -= 1
            self.save()
            return 'commented deleted successfully'
        else:
            return 'no comment found!'
            

    def delete_post(self, user):
        self.delete()
        user.posts_count -=1
        user.save()
        


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    post = models.ForeignKey(
        Post, related_name='post_attachments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        to=User, related_name='post_attachments', on_delete=models.CASCADE)

    def image_link(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('created_by', 'post')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_ago(self):
        return timesince(self.created_at)

    class Meta:
        ordering = ('created_at',)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, related_name='reports', on_delete=models.CASCADE)
    report = models.TextField()
    created_by = models.ForeignKey(
        User, related_name='reports', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Trend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()
