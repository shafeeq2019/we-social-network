from django.db import migrations, models


class Migration(migrations.Migration):
    # Removes the duplicated 'post_comment' choice (no database change)

    dependencies = [
        ('notification', '0002_rename_post_id_notification_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('new_friendrequest', 'New friendrequest'), ('accepted_friendrequest', 'Accepted friendrequest'), ('rejected_friendrequest', 'Rejected friendrequest'), ('post_like', 'Post like'), ('post_comment', 'Post comment')], max_length=50),
        ),
    ]
