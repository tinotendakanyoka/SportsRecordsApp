# Generated by Django 5.0.3 on 2024-03-08 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_record_event_record_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='core.event'),
        ),
    ]
