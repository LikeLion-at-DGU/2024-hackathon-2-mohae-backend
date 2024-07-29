# Generated by Django 5.0.3 on 2024-07-25 21:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='culturalactivity',
            name='available_slots',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Confirmed'), ('N', 'Cancelled')], default='P', max_length=1),
        ),
        migrations.CreateModel(
            name='ConfirmedReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed_at', models.DateTimeField(auto_now_add=True)),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='culture.reservation')),
            ],
        ),
    ]
