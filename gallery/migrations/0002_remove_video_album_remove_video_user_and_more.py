# Generated by Django 5.0.7 on 2024-07-31 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='album',
        ),
        migrations.RemoveField(
            model_name='video',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='video',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='video',
        ),
        migrations.DeleteModel(
            name='PhotoVideoLike',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]