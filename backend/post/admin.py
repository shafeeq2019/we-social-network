from django.contrib import admin
from .models import Post, PostAttachment, Like, Comment, Report, Trend

# Register your models here.

admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Trend)