from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    name = models.CharField(primary_key=True, max_length=255, blank=True)
    event_num = models.IntegerField(blank=False)   #, unique=True
    is_boys_event = models.BooleanField(default=False)  
    event_year = models.IntegerField(default=timezone.now().year)

    
    def __str__(self):
        return f"{self.name}"
    

class House(models.Model):
    name = models.CharField(max_length=255)
    points = models.FloatField(default=0, null=False)
    position = models.IntegerField(default=4)

    def determine_position(self):
        all_houses_queryset = self.objects.all()
        


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.BooleanField(default=False) 
    points = models.IntegerField(default=0)
    
    
    def __str__(self):
        return f"{self.full_name}"
    
    


class EventParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    laptime_or_distance = models.CharField(max_length=255, default='')

    class Meta:
        unique_together = (('event', 'student'),)  

    def __str__(self):
        return f"{self.student.full_name} participating in {self.event.name}"
