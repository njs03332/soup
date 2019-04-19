# Generated by Django 2.2 on 2019-04-19 10:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsdiary', '0005_event_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
