from .models import Post, Comment
from rest_framework import serializers
from account.serializers import UserSerializer
from django.utils.timesince import timesince

# class PostSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     created_at_ago = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id', 'body', 'created_by', 'created_at', 'created_at_ago']

#     def get_created_at_ago(self, obj):
#         now = datetime.now(timezone.utc)  # Make sure it's also aware
#         return timesince(obj.created_at, now)


class PostSerializer(serializers.ModelSerializer):
    # Du kannst das created_by Feld hier entfernen, da wir es dynamisch in der __init__ Methode setzen werden.
    post_liked = serializers.BooleanField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at', 'created_ago',
                  'created_by', 'likes_count', 'post_liked', 'comments_count']

    def __init__(self, *args, show_created_by=False, **kwargs):
        super().__init__(*args, **kwargs)

        if show_created_by:
            self.fields['created_by'] = UserSerializer(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'created_by', 'created_ago']


class PostDetailSerializer(serializers.ModelSerializer):
    post_liked = serializers.BooleanField(required=False)
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_at', 'created_ago', 'created_by',
                  'likes_count', 'post_liked', 'comments_count', 'comments']
