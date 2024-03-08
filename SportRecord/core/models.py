from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime
from django.db.models.signals import pre_save
from django.forms import ChoiceField
from django.db.models import Q

AGE_GROUPS = (
    ("U14", "U14"),
    ("U15", "U15"),
    ("U16", "U16"),
    ("U17", "U17"),
    ("U18", "U18"),
    ("U20", "U20"),
    ("OPEN", "OPEN"),

)

class AgeGroup(models.Model):
    name = models.CharField(max_length=255, choices=AGE_GROUPS)

    def __str__(self):
        return self.name

# Create your models here.
class Event(models.Model):
    name = models.CharField(primary_key=True, max_length=255, blank=True)
    event_num = models.IntegerField(blank=False)   #, unique=True
    is_boys_event = models.BooleanField(default=False)  
    event_year = models.IntegerField(default=timezone.now().year)

class AgeGroupEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.event.name} {self.age_group.name}"
    

HOUSE_CHOICES = (
    ("MICHAEL", "MICHAEL"),
    ("GABRIEL", "GABRIEL"),
    ("RAPHAEL", "RAPHAEL"),
)

class House(models.Model):
    name = models.CharField(max_length=255, choices=HOUSE_CHOICES)
    points = models.FloatField(default=0, null=False)
    house_color = models.CharField(max_length=25, null=False, blank=False, default='red')
    position = models.IntegerField(default=4)


    def determine_position(self):
        ordered_houses_queryset = enumerate(self.objects.order_by("-points"), start=1)

        for index, house in ordered_houses_queryset:
            house.position == index
            house.save()

    def __str__(self):
        return f'{self.name}: {self.points} Points'

        
GENDER_CHOICES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
)

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(choices = GENDER_CHOICES, max_length=10)
    points = models.IntegerField(default=0)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='students')
    
    
    def __str__(self):
        return f"{self.full_name}"
    

class Record(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='records')
    event = models.OneToOneField(AgeGroupEvent, on_delete=models.CASCADE, related_name='record')
    time_or_distance = models.CharField(max_length=255)
    event_year = models.IntegerField(default=timezone.now().year)

    def __str__(self):
        return f'{self.student.full_name} - {self.event.event.name} : {self.time_or_distance}'
    
    

class EventParticipation(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(AgeGroupEvent, on_delete=models.CASCADE, blank=True, related_name='events')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, related_name='event')
    attempt1  = models.CharField(max_length=255, default='0m')
    attempt2  = models.CharField(max_length=255, default='0m')
    attempt3  = models.CharField(max_length=255, default='0m')
    laptime_or_distance = models.CharField(max_length=255, default='0m')
    position = models.IntegerField(default=0)

    
    
    class Meta:
        unique_together = (('event', 'student'),)  

    def __str__(self):
        return f"{self.student.full_name} participating in {self.event.name}"


    def calculate_position(self):
        """Calculates and updates the position based on attempts."""
        attempts = [self.attempt1, self.attempt2, self.attempt3]
        best_attempt = max(attempts)
        print(best_attempt)
        self.laptime_or_distance = str(best_attempt)  # Convert to string


        rankings = EventParticipation.objects.filter(event=self.event).order_by('-laptime_or_distance')
        for i, obj in enumerate(rankings, start=1):
            if obj == self:
                self.position = i
                break



        # # Rank positions based on best attempts (lower is better)
        # rankings = EventParticipation.objects.filter(event=self.event).order_by('laptime_or_distance')
        # self.position = rankings.index(self) + 1  # Add 1 for starting from 1

        self.save()

    # def __str__(self):
    #     return f"{self.student} - {self.laptime_or_distance}"

def validate_eventparticipation(sender,instance, **kwargs):    

    studentperson = instance.student
    eventqualified = instance.event
    pos_attained = int(instance.position)
    laptime_distance = instance.laptime_or_distance  
   
         
    hsepts =0  
    
    if pos_attained == 1:
        hsepts = 6
    elif pos_attained == 2:
        hsepts = 5
    elif pos_attained == 3:
        hsepts = 4
    elif pos_attained == 4:
        hsepts = 3
    elif pos_attained == 5:
        hsepts = 2
    elif pos_attained == 6:
        hsepts = 1
        
    current_student_pts =  int(studentperson.points)
    points_update = current_student_pts + hsepts 
    Student.objects.filter(full_name=studentperson.full_name).update(points=points_update)
    print(studentperson.full_name, '  now has ',studentperson.points, ' points' )
       
      
    current_house_pts =  studentperson.house.points
    house_points_update = current_house_pts + hsepts 
    House.objects.filter(name=studentperson.house.name).update(points=house_points_update)
    print(studentperson.house.name, '  now has ',studentperson.house.points , ' points' )
    # else:
    #     current_gpts =  studentperson.hse.girl_pts
    #     g_points_update = current_gpts + hsepts 
    #     House.objects.filter(name=studentperson.hse.name).update(girl_pts=g_points_update)
    #     print(studentperson.hse.name, '  now has ',studentperson.hse.girl_pts , ' points' )
        

    #Capturing Current Record
    current_laptime_distance = eventqualified.record.time_or_distance
    if "m" in current_laptime_distance:
        record_distance = current_laptime_distance
    else:
        record_time = current_laptime_distance
        print(record_time, ' is the record time')
        
    
    
    
    
    if "m" in laptime_distance:
          # Distance input (in meters)
          try:
            laptime_distance.replace(",", ".")
            user_distance = float(laptime_distance.split("m")[0])
            record_distance = float(record_distance.split("m")[0])
            
            if user_distance > record_distance:
              message = "Congratulations! new record"
              Record.objects.filter(event=eventqualified.event.name).update(description=studentperson.full_name)
              Record.objects.filter(event=eventqualified.event.name).update(time_or_distance=laptime_distance)
              Record.objects.filter(event=eventqualified.event.name).update(event_year=timezone.now().year)
              Record.objects.filter(event=eventqualified.event.name).update(student=studentperson)




          except ValueError:
            message = "Invalid input for distance. Please enter a number followed by 'm'."
    
    elif ":" in laptime_distance:
      # Time input (in minutes:seconds)
     
            
     # try:
   
    
        user_minutesR, user_seconds_with_millisecondsR = record_time.split(":")
        print(user_minutesR, user_seconds_with_millisecondsR, ' split time')
        user_secondsR, user_millisecondsR = user_seconds_with_millisecondsR.split(".")
        user_timeR = datetime.strptime(f"{user_minutesR}:{user_secondsR}.{user_millisecondsR}", "%M:%S.%f").time()
        print(record_time, ' is the record time and splits  ', user_timeR)  
        
        
        print(laptime_distance, '   is the laptop distance')
    
        user_minutes, user_seconds_with_milliseconds = laptime_distance.split(":")
        user_seconds, user_milliseconds = user_seconds_with_milliseconds.split(".")
        
        user_time = datetime.strptime(f"{user_minutes}:{user_seconds}.{user_milliseconds}", "%M:%S.%f").time()
        print(user_time, ' is the user time and splits  ', user_time)  
      
        if user_time < user_timeR:
            # time_difference = record_time - user_time
            # minutes, seconds = divmod(time_difference.seconds, 60)
            # milliseconds = time_difference.microseconds // 1000   
            Record.objects.filter(event=eventqualified.event.name).update(name=studentperson.full_name)
            Record.objects.filter(event=eventqualified.event.name).update(time_or_distance=user_time)
            Record.objects.filter(event=eventqualified.event.name).update(event_year=timezone.now().year)
           # Record.objects.filter(event=eventqualified.record.event).update(event_year=timezone.now().year)
    
    
            
            message = "Congratulations"
        else:
            message = "The record time is {}. Try again!".format(record_time)
          
      # except ValueError:
      #     message = "Invalid input for time. Please enter in minutes:seconds format (e.g., 00:10.00)."


        
pre_save.connect(validate_eventparticipation, sender=EventParticipation)