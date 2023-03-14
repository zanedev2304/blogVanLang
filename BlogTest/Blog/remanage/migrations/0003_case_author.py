# Generated by Django 4.1.7 on 2023-03-14 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remanage', '0002_rename_name_casestatus_status_case_handler_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases_created', to=settings.AUTH_USER_MODEL),
        ),
    ]