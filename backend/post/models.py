from django.db import models
import uuid
from account.models import User
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
            return "post liked successfully"

    def add_comment(self, user, comment):
        Comment.objects.create(created_by=user, post=self, comment=comment)
        self.comments_count += 1
        self.save()
        return 'post commented successfully'


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    post = models.ForeignKey(
        Post, related_name='post_attachments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        to=User, related_name='post_attachments', on_delete=models.CASCADE)
    
    def image_link(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
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


class Trend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()
