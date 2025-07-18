# Generated by Django 4.2.23 on 2025-07-07 18:09

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_alter_trip_trip_name_alter_trip_vehicle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['-travel_datetime']},
        ),
        migrations.RemoveField(
            model_name='trip',
            name='travel_date',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='travel_time',
        ),
        migrations.AlterField(
            model_name='trip',
            name='travel_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='trip_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
    ]
