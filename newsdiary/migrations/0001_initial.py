# Generated by Django 2.2 on 2019-04-19 12:26

import datetime
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('press', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('url', models.URLField(default='https://www.naver.com')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('explanation', models.TextField(blank=True)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('POL', '정치'), ('SOC', '사회'), ('ECON', '경제'), ('WRD', '세계')], max_length=20), default=list, size=None)),
                ('followers', models.ManyToManyField(blank=True, related_name='following_issues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Noti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=100)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_newsdiary.noti_set+', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('gender', models.CharField(blank=True, max_length=20)),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(1)])),
                ('noti_time', models.TimeField(default=datetime.time(10, 0))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='새로운 메모', max_length=20)),
                ('content', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memos', to='newsdiary.Article')),
                ('issue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memos', to='newsdiary.Issue')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='memos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Journalist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='newsdiary.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('datetime', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
                ('concept', models.TextField(blank=True)),
                ('background', models.TextField(blank=True)),
                ('importance', models.TextField(blank=True)),
                ('explanation', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('POL', '정치'), ('SOC', '사회'), ('ECON', '경제'), ('WRD', '세계')], max_length=20)),
                ('followers', models.ManyToManyField(blank=True, related_name='following_events', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='newsdiary.Issue')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='newsdiary.Event'),
        ),
        migrations.AddField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='newsdiary.Issue'),
        ),
        migrations.AddField(
            model_name='article',
            name='parent_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='top_article', to='newsdiary.Event'),
        ),
        migrations.CreateModel(
            name='NonregularNoti',
            fields=[
                ('noti_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='newsdiary.Noti')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='newsdiary.Event')),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='newsdiary.Issue')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('newsdiary.noti',),
        ),
    ]
