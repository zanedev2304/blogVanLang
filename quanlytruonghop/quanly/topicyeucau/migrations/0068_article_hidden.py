# Generated by Django 4.2.1 on 2023-05-15 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicyeucau', '0067_remove_knowledge_is_featured_remove_knowledge_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]