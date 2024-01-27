from .models import Post, Comment, Trend, PostAttachment
from rest_framework import serializers
from account.serializers import UserSerializer
from django.utils.timesince import timesince

class PostAttachment(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ['id', 'image_link']


class PostSerializer(serializers.ModelSerializer):
    # Du kannst das created_by Feld hier entfernen, da wir es dynamisch in der __init__ Methode setzen werden.
    post_liked = serializers.BooleanField(required=False)
    post_attachments = PostAttachment(read_only=True, many=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at', 'created_ago',
                  'created_by', 'likes_count', 'post_liked', 'comments_count', 'post_attachments','is_private']

    # def __init__(self, *args, show_created_by=False, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     if show_created_by:
    #         self.fields['created_by'] = UserSerializer(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'created_by', 'created_ago']


class PostDetailSerializer(serializers.ModelSerializer):
    post_liked = serializers.BooleanField(required=False)
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    post_attachments = PostAttachment(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at', 'created_ago', 'created_by',
                  'likes_count', 'post_liked', 'comments_count', 'comments', 'post_attachments']


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ['id', 'hashtag', 'occurences']
