from django.contrib import admin
from .models import Student, Event, EventParticipation, House, Record, AgeGroup, AgeGroupEvent


admin.site.register(Student)
admin.site.register(Event)
admin.site.register(EventParticipation)
admin.site.register(House)
admin.site.register(Record)
admin.site.register(AgeGroup)
admin.site.register(AgeGroupEvent)