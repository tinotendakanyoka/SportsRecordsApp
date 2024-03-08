# Generated by Django 5.0.3 on 2024-03-08 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_record_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipation',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='core.student'),
        ),
    ]
