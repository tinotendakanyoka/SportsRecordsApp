# Generated by Django 5.0.3 on 2024-03-08 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_record_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='core.event'),
        ),
    ]
