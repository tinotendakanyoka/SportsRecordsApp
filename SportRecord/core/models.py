from django.db import models
from django.utils import timezone

# Create your models here.

class AgeGroup(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, default='')
    earliest_dob = models.DateField()
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Male'),
        ('F', 'Female')])

    def __str__(self):
        return f'{self.title} Boys' if self.gender == 'M' else f'{self.title} Girls'

class CompetitiveHouse(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    color = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name



class AthleticEvent(models.Model):
    title = models.CharField(max_length=255)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    current_record_holder_name = models.CharField(max_length=255)
    current_record = models.FloatField()
    record_date = models.DateField()
    is_track_event = models.BooleanField(default=False)

    class Meta:
        unique_together = ['title', 'age_group']

    def __str__(self):
        return f'{self.age_group} {self.title}'




class Participant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    date_of_birth = models.DateField()

    gender = models.CharField(max_length=1, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
    ])
    competitive_house = models.ForeignKey(CompetitiveHouse, on_delete=models.CASCADE)
    individual_points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Record(models.Model):
    event = models.OneToOneField(AthleticEvent, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    record = models.FloatField()
    record_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.participant} - {self.event} - {self.record}'
    

from django.db import models
from django.utils import timezone

class EventParticipation(models.Model):
    event = models.ForeignKey(AthleticEvent, on_delete=models.CASCADE, related_name='participations')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    attempt1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempt2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempt3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    best_attempt = models.FloatField(default=0.00)
    athlete_position = models.IntegerField(default=0)

    class Meta:
        unique_together = ['event', 'participant']

    from django.db import models
from django.utils import timezone

class EventParticipation(models.Model):
    event = models.ForeignKey(AthleticEvent, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    attempt1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempt2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempt3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    best_attempt = models.FloatField(default=0.00)
    athlete_position = models.IntegerField(default=0)

    class Meta:
        unique_together = ['event', 'participant']

    def save(self, *args, **kwargs):
        """ Update best attempt before saving """
        self.best_attempt = max(self.attempt1, self.attempt2, self.attempt3)
        super().save(*args, **kwargs)

        # **Update rankings efficiently**
        

    def __str__(self):
        return f'{self.participant} - {self.event}'


    def __str__(self):
        return f'{self.participant} - {self.event}'

    
# post_save function to rank participants in an event and assign points to house and individual
