
from django.shortcuts import render, redirect
from django.views import View
from .models import AthleticEvent as Event, Participant as Student, EventParticipation, CompetitiveHouse as House, AgeGroup
from .forms import EventForm, StudentForm, EventParticipationForm
from django.forms import modelformset_factory
from django.db.models import Q
import datetime
from django.http import JsonResponse
from .utils import initialize_data
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import EventParticipationSerializer, ParticipantSerializer

from rest_framework.views import APIView
from rest_framework.response import Response





    
    


def dashboard(request):
    boys_events_qs = Event.objects.filter(age_group__gender='M').order_by('title')
    girls_events_qs = Event.objects.filter(age_group__gender='F').order_by('title')
    recent_event_winners = EventParticipation.objects.filter(athlete_position=1)
    top_performers = Student.objects.all().order_by('-individual_points')


    ordered_houses = enumerate(House.objects.all().order_by('-points'), start=1)
    context = {
        'houses': ordered_houses,
        'boys_events': boys_events_qs,
        'girls_events': girls_events_qs,
        'recent_events': recent_event_winners,
        'top_performers': top_performers,
    }

    return render(request, 'core/index.html', context)



class EligibleParticipantsView(ListAPIView):
    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(pk=event_id)
        age_group = event.age_group
        return Student.objects.filter(Q(date_of_birth__gte=age_group.earliest_dob, gender=age_group.gender))
    serializer_class = ParticipantSerializer


def initialize(request):
    initialize_data()

    return redirect('dashboard')

class EventParticipationListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(pk=event_id)
        return EventParticipation.objects.filter(event=event)
    serializer_class = EventParticipationSerializer



def event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'core/event.html', {'event': event})