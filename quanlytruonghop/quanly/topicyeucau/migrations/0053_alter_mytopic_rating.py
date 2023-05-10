# Generated by Django 4.2 on 2023-05-04 22:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicyeucau', '0052_mytopic_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytopic',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
