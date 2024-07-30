# Generated by Django 5.0.7 on 2024-07-29 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='family',
            name='members',
        ),
        migrations.RemoveField(
            model_name='family',
            name='invite_code',
        ),
        migrations.AlterField(
            model_name='family',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='families', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FamilyMembership',
        ),
    ]
