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
        all_event_participants = list(EventParticipation.objects.filter(event=self.event).order_by('-best_attempt'))
        
        # Assign rankings
        for index, event_participant in enumerate(all_event_participants):
            event_participant.athlete_position = index + 1

        # **Bulk update to save all rankings in a single query**
        EventParticipation.objects.bulk_update(all_event_participants, ['athlete_position'])

        # **Update points for top 8 positions**
        points_map = {1: 9, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
        participants_to_update = []

        for event_participant in all_event_participants:
            position = event_participant.athlete_position

            if position == 1 and event_participant.best_attempt > event_participant.event.current_record:
                record, created = Record.objects.get_or_create(
                    event=event_participant.event,
                    participant=event_participant.participant,
                    record=event_participant.best_attempt,
                    record_date=timezone.now()
                )
                event_participant.event.current_record_holder_name = (
                    f'{event_participant.participant.first_name} {event_participant.participant.last_name}'
                )
                event_participant.event.current_record = event_participant.best_attempt
                event_participant.event.record_date = timezone.now()
                event_participant.event.save()
                points = 10  # Ten points for broken record

            # Update individual and house points
                event_participant.participant.individual_points += points
                event_participant.participant.competitive_house.points += points
            
            else:

                points = points_map.get(position, 0)  # Default to 0 if out of top 8

            # Update individual and house points
                event_participant.participant.individual_points += points
                event_participant.participant.competitive_house.points += points

            participants_to_update.append(event_participant.participant)
            participants_to_update.append(event_participant.participant.competitive_house)

            # **Check for new event record**
            

        # **Bulk update participant and house points in a single query**
        Participant.objects.bulk_update(
            [p for p in participants_to_update if isinstance(p, Participant)], 
            ['individual_points']
        )
        CompetitiveHouse.objects.bulk_update(
            [p for p in participants_to_update if isinstance(p, CompetitiveHouse)], 
            ['points']
        )

    def __str__(self):
        return f'{self.participant} - {self.event}'

    
# post_save function to rank participants in an event and assign points to house and individual
