# Generated by Django 4.2.23 on 2025-07-12 14:42

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0009_alter_trip_status_alter_trip_trip_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
    ]
