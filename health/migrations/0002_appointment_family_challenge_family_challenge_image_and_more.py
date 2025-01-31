# Generated by Django 5.0.7 on 2024-08-04 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0001_initial'),
        ('users', '0002_alter_family_family_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.family'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.family'),
        ),
        migrations.AddField(
            model_name='medication',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.family'),
        ),
    ]
