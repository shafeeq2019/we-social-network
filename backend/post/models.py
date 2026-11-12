from django.db import IntegrityError, models, transaction
import uuid
from account.models import User
from django.conf import settings
from django.utils.timesince import timesince

# Create your models here.


class PostQuerySet(models.QuerySet):
    def visible_to(self, user):
        # Private posts are only visible to their author
        return self.filter(models.Q(is_private=False) | models.Q(created_by=user))

    def with_details(self, user):
        # Loads everything PostSerializer needs in a fixed number of queries:
        # author via JOIN, attachments in one extra query and post_liked as a
        # subquery instead of one query per post
        return self.select_related('created_by').prefetch_related('post_attachments').annotate(
            post_liked=models.Exists(
                Like.objects.filter(post=models.OuterRef('pk'), created_by=user)))


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)

    def created_ago(self):
        return timesince(self.created_at)

    def _change_count(self, field, delta):
        # Atomic UPDATE ... SET x = x + delta in the database. A read-modify-write
        # (x += 1; save()) loses updates when two requests run at the same time,
        # and a full save() would also overwrite the other counters with stale values.
        Post.objects.filter(pk=self.pk).update(**{field: models.F(field) + delta})
        self.refresh_from_db(fields=[field])

    def add_like(self, user):
        # Toggles the like. Deleting first and treating a unique violation as
        # "already liked" means a double click can't create a duplicate or a 500.
        with transaction.atomic():
            deleted, _ = self.likes.filter(created_by=user).delete()
            if deleted:
                self._change_count('likes_count', -1)
                return "post disliked successfully"

            try:
                with transaction.atomic():
                    Like.objects.create(post=self, created_by=user)
            except IntegrityError:
                # A parallel request created the like in the meantime
                return "post liked successfully"

            self._change_count('likes_count', 1)

        self.notifications.create_notification(
            created_by=user, created_for=self.created_by, type_of_notification='post_like')
        return "post liked successfully"

    def add_comment(self, user, comment):
        Comment.objects.create(created_by=user, post=self, comment=comment)
        self._change_count('comments_count', 1)
        self.notifications.create_notification(
            created_by=user, created_for=self.created_by, type_of_notification='post_comment')
        return 'post commented successfully'

    def delete_comment(self, user, comment_id):
        # The post author can delete every comment, others only their own
        comments = self.comments.all()
        if user != self.created_by:
            comments = comments.filter(created_by=user)

        # delete() returns 0 if a parallel request already removed it
        deleted, _ = comments.filter(id=comment_id).delete()
        if not deleted:
            return False

        self._change_count('comments_count', -1)
        return True

    def delete_post(self, user):
        self.delete()
        User.objects.filter(pk=user.pk).update(posts_count=models.F('posts_count') - 1)


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
