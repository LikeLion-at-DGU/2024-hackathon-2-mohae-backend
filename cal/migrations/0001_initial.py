# Generated by Django 5.0.3 on 2024-08-03 15:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('emoji', models.TextField(blank=True, null=True)),
                ('emoji_text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='Y', max_length=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to=settings.AUTH_USER_MODEL)),
                ('family_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.family')),
                ('participants', models.ManyToManyField(blank=True, related_name='calendar_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
