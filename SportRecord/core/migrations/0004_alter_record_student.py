# Generated by Django 5.0.3 on 2024-03-08 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_record_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='core.student'),
        ),
    ]
