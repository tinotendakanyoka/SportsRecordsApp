# Generated by Django 5.1.7 on 2025-03-14 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('earliest_dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='CompetitiveHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('points', models.IntegerField(default=0)),
                ('color', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AthleticEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('current_record_holder_name', models.CharField(max_length=255)),
                ('current_record', models.FloatField()),
                ('record_date', models.DateField()),
                ('is_track_event', models.BooleanField(default=False)),
                ('age_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.agegroup')),
            ],
            options={
                'unique_together': {('title', 'age_group')},
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('individual_points', models.IntegerField(default=0)),
                ('competitive_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competitivehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.FloatField()),
                ('record_date', models.DateField()),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.athleticevent')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.participant')),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt1', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('attempt2', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('attempt3', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('best_attempt', models.FloatField()),
                ('athlete_position', models.IntegerField(default=6)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.athleticevent')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.participant')),
            ],
            options={
                'unique_together': {('event', 'participant')},
            },
        ),
    ]
