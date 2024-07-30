# Generated by Django 5.0.3 on 2024-07-26 17:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoVideoLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_video_likes', to='gallery.photo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_video_likes', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_video_likes', to='gallery.video')),
            ],
            options={
                'unique_together': {('user', 'photo'), ('user', 'video')},
            },
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]