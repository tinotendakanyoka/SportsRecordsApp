from django.db import models
from django import forms


EVENT_TYPES = (
    ('1', 'GENDER_EVENT_NAME'),
)
AGE_GROUPS = (
    ("13 - 14", "UNDER 14"),

)

class Event(models.Model):
    event_type = forms.ChoiceField(choices = EVENT_TYPES)

class Student(models.Model):
    pass

class House(models.Model):
    pass

class Record(models.Model):

    full_name = models.CharField(max_length=255)
    age_group = forms.ChoiceField(choices = AGE_GROUPS)
    def __str__(self):
        return f'{self}'