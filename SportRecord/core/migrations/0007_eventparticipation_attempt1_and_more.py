# Generated by Django 5.0.3 on 2024-03-08 05:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_house_house_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparticipation',
            name='attempt1',
            field=models.CharField(default='0m', max_length=255),
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='attempt2',
            field=models.CharField(default='0m', max_length=255),
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='attempt3',
            field=models.CharField(default='0m', max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='house',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.house'),
        ),
        migrations.AlterField(
            model_name='eventparticipation',
            name='event',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.event'),
        ),
        migrations.AlterField(
            model_name='eventparticipation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='eventparticipation',
            name='laptime_or_distance',
            field=models.CharField(default='0m', max_length=255),
        ),
        migrations.AlterField(
            model_name='eventparticipation',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.student'),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_or_distance', models.CharField(max_length=255)),
                ('event_year', models.IntegerField(default=2024)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
        ),
    ]
