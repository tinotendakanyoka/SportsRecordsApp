# Generated by Django 5.0.3 on 2024-03-08 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_eventparticipation_event_alter_record_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='description',
        ),
    ]
