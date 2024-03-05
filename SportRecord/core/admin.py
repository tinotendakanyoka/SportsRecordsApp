from django.contrib import admin
from .models import Student, Event, EventParticipation, House


admin.site.register(Student)
admin.site.register(Event)
admin.site.register(EventParticipation)
admin.site.register(House)

