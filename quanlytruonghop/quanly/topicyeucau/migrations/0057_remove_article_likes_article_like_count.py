# Generated by Django 4.2 on 2023-05-05 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicyeucau', '0056_article_likes_article_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.AddField(
            model_name='article',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]