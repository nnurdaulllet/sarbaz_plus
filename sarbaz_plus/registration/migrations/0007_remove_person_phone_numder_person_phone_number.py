# Generated by Django 5.2 on 2025-05-03 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_person_phone_numder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='phone_numder',
        ),
        migrations.AddField(
            model_name='person',
            name='phone_number',
            field=models.BigIntegerField(default=87777777777, max_length=12),
            preserve_default=False,
        ),
    ]
