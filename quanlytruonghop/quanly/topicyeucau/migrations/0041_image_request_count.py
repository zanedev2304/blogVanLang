# Generated by Django 4.2 on 2023-05-03 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicyeucau', '0040_category_alter_topic_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='request_count',
            field=models.IntegerField(default=0),
        ),
    ]