from django.contrib import admin
from .models import Participant as Student, AthleticEvent as Event, EventParticipation, CompetitiveHouse as House, Record, AgeGroup


admin.site.register(Student)
admin.site.register(Event)
admin.site.register(EventParticipation)
admin.site.register(House)
admin.site.register(Record)
admin.site.register(AgeGroup)
