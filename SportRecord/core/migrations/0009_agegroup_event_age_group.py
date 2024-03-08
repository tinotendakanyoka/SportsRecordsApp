# Generated by Django 5.0.3 on 2024-03-08 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_record_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('U14', 'U14'), ('U15', 'U15'), ('U16', 'U16'), ('U17', 'U17'), ('U18', 'U18'), ('U20', 'U20'), ('OPEN', 'OPEN')], max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='age_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.agegroup'),
            preserve_default=False,
        ),
    ]
