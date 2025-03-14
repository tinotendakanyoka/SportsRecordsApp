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
    

class EventParticipation(models.Model):
    event = models.ForeignKey(AthleticEvent, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    attempt1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempt2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attempt3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    best_attempt = models.FloatField(default=0.00)
    athlete_position = models.IntegerField(default=6)

    class Meta:
        unique_together = ['event', 'participant']

    def save(self, *args, **kwargs):
        self.best_attempt = max(self.attempt1, self.attempt2, self.attempt3)
        super().save(*args, **kwargs)  # Save the current instance first

        # Update athlete positions and points
        all_event_participants = EventParticipation.objects.filter(event=self.event).order_by('-best_attempt')
        for index, event_participant in enumerate(all_event_participants):
            event_participant.athlete_position = index + 1

            # Update points for house and individual
            if event_participant.athlete_position == 1:
                if event_participant.best_attempt > event_participant.event.current_record:
                    record, created = Record.objects.get_or_create(
                        event=event_participant.event,
                        participant=event_participant.participant,
                        record=event_participant.best_attempt,
                        record_date=timezone.now()
                    )
                    record.save()
                    event_participant.event.current_record_holder_name = f'{event_participant.participant.first_name} {event_participant.participant.last_name}'
                    event_participant.event.current_record = event_participant.best_attempt
                    event_participant.event.record_date = timezone.now()
                    event_participant.event.save()
                    event_participant.participant.individual_points += 10
                    event_participant.participant.competitive_house.points += 10
                else:
                    event_participant.participant.individual_points += 9
                    event_participant.participant.competitive_house.points += 9
            elif event_participant.athlete_position == 2:
                event_participant.participant.individual_points += 7
                event_participant.participant.competitive_house.points += 7
            elif event_participant.athlete_position == 3:
                event_participant.participant.individual_points += 6
                event_participant.participant.competitive_house.points += 6
            elif event_participant.athlete_position == 4:
                event_participant.participant.individual_points += 5
                event_participant.participant.competitive_house.points += 5
            elif event_participant.athlete_position == 5:
                event_participant.participant.individual_points += 4
                event_participant.participant.competitive_house.points += 4
            elif event_participant.athlete_position == 6:
                event_participant.participant.individual_points += 3
                event_participant.participant.competitive_house.points += 3
            elif event_participant.athlete_position == 7:
                event_participant.participant.individual_points += 2
                event_participant.participant.competitive_house.points += 2
            elif event_participant.athlete_position == 8:
                event_participant.participant.individual_points += 1
                event_participant.participant.competitive_house.points += 1
            else:
                event_participant.participant.individual_points += 0
                event_participant.participant.competitive_house.points += 0

            # Save the participant and house points without calling save on EventParticipation again
            event_participant.participant.save()
            event_participant.participant.competitive_house.save()
    
    # validate age group when model is created


    def __str__(self):
        return f'{self.participant} - {self.event}'
    
# post_save function to rank participants in an event and assign points to house and individual
