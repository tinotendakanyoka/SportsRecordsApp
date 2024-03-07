from django.contrib import admin
from .models import Student, Event, EventParticipation, House, Record


admin.site.register(Student)
admin.site.register(Event)
admin.site.register(EventParticipation)
admin.site.register(House)
admin.site.register(Record)
