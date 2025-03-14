
from django.shortcuts import render, redirect
from django.views import View
from .models import AthleticEvent as Event, Participant as Student, EventParticipation, CompetitiveHouse as House, AgeGroup
from .forms import EventForm, StudentForm, EventParticipationForm
from django.forms import modelformset_factory
from django.db.models import Q
import datetime
from django.http import JsonResponse
from .utils import initialize_data


class UpdateEventsView(View):
    def get(self, request):
        queryset = Event.objects.all().order_by('event_year')
        formset = modelformset_factory(Event, form=EventForm , extra=0)

        formset = formset(queryset=queryset)
        return render(request, 'core/update_event.html', {'formset': formset})

    def post(self, request):
        formset = modelformset_factory(Event, form=EventForm)
        formset = formset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect('events_update')
        return render(request, 'core/update_event.html', {'formset': formset})






class UpdateStudentsView(View):
    def get(self, request):
        queryset = Student.objects.all().order_by('date_of_birth')
        formset = modelformset_factory(Student, form=StudentForm , extra=0)

        formset = formset(queryset=queryset)
        return render(request, 'update_event.html', {'formset': formset})

    def post(self, request):
        formset = modelformset_factory(Student, form=StudentForm)
        formset = formset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect('students_update')
        return render(request, 'update_event.html', {'formset': formset})
    
    


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

def CreateMultipleParticipationsView(request, event_id):

    event = Event.objects.get(pk=event_id)  
    EventParticipationFormSet = modelformset_factory(EventParticipation, fields=('id', 'event', 'student', 'attempt1', 'attempt2', 'attempt3', 'laptime_or_distance', 'position') , extra=12)
    form = EventParticipationFormSet(queryset=EventParticipation.objects.none(), initial=[{'event': event}]) 


    if request.method =='POST':
        form = EventParticipationFormSet(request.POST)

        try:

            form.save(commit=False)
            for instance in form:
                if not instance.is_valid():
                    pass
                    
                elif instance.is_valid():
                    instance.save()
        except:
            pass
 
    
        

    return render(request, 'core/create_event.html', {'form': form})

    # event = Event.objects.get(name=event_name)  
    # EventParticipationFormSet = modelformset_factory(EventParticipation, fields=('id', 'event', 'student', 'attempt1', 'attempt2', 'attempt3', 'laptime_or_distance', 'position') , extra=12)
    # form = EventParticipationFormSet(queryset=EventParticipation.objects.none(), initial=[{'event': event}]) 


    # if request.method =='POST':
    #     form = EventParticipationFormSet(request.POST)

    #     try:

    #         form.save(commit=False)
    #         for instance in form:
    #             if not instance.is_valid():
    #                 pass
                    
    #             elif instance.is_valid():
    #                 instance.save()
    #     except:
    #         pass
    #     return redirect('edit_data') 

def register_participants(request, age_group, gender, event_name):

    gender = gender.upper()

    if request.method == 'GET':
        match age_group:
            case "u14":
                after_date = datetime.date(year=2010, month=3, day=9)
                eligible_participants = Student.objects.filter(date_of_birth__gt=after_date, gender=gender)
            case "u15":
                after_date = datetime.date(year=2009, month=3, day=9)
                eligible_participants = Student.objects.filter(date_of_birth__gt=after_date, gender=gender)
            case "u16":
                after_date = datetime.date(year=2008, month=3, day=9)
                eligible_participants = Student.objects.filter(date_of_birth__gt=after_date, gender=gender)
            case "u17":
                after_date = datetime.date(year=2007, month=3, day=9)
                eligible_participants = Student.objects.filter(date_of_birth__gt=after_date, gender=gender)
            case "u18":
                after_date = datetime.date(year=2006, month=3, day=9)
                eligible_participants = Student.objects.filter(date_of_birth__gt=after_date, gender=gender)
            case "u20":
                after_date = datetime.date(year=2005, month=3, day=9)
                eligible_participants = Student.objects.filter(date_of_birth__gt=after_date, gender=gender)
            case "open":
                eligible_participants = Student.objects.filter(gender=gender)

        context = {
            'students': eligible_participants,
        }


        return render(request, 'core/register_participants.html', context = context)
    
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode("utf-8"))
        student = Student.objects.get(full_name=data["student"])
        event = Event.objects.get(name=event_name)
        #event = AgeGroupEvent.objects.filter(event=event, age_group__name=age_group)

        if EventParticipation.objects.filter(event=event, student=student).exists():
            return JsonResponse({
                "error": "Student Already Registered"
            })

        else:
            event_pariticip = EventParticipation(event=event, student=student)
            event_pariticip.save()

            return JsonResponse({
                "Success": True,
                "message": "Student Registered",

            })


        # return JsonResponse({
        #     "Event": event_name,
        #     "message": request.POST['student'],
        # })


def initialize(request):
    initialize_data()

    return redirect('dashboard')