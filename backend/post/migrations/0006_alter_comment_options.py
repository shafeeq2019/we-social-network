# Generated by Django 5.0 on 2024-01-04 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_post_comments_count_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]