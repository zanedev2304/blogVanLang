# Generated by Django 4.2 on 2023-05-06 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicyeucau', '0058_article_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(default='other', max_length=255),
        ),
        migrations.AlterField(
            model_name='knowledge',
            name='category',
            field=models.CharField(default='other', max_length=255),
        ),
    ]