# Generated by Django 4.1.7 on 2023-03-27 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topicyeucau', '0012_alter_topic_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='image',
        ),
    ]
