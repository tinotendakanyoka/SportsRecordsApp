
from django.shortcuts import render, redirect
from django.views import View
from .models import Event, Student, EventParticipation, House
from .forms import EventForm, StudentForm, EventParticipationForm
from django.forms import modelformset_factory
from django.db.models import Q

# class UpdateEventsView(View):
#     def get(self, request):
#         queryset = Event.objects.all().order_by('event_year')
#         formset = modelformset_factory(Event, form=EventForm , extra=0)

#         formset = formset(queryset=queryset)
#         return render(request, 'core/update_event.html', {'formset': formset})

#     def post(self, request):
#         formset = modelformset_factory(Event, form=EventForm)
#         formset = formset(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 if form.is_valid():
#                     form.save()
#             return redirect('events_update')
#         return render(request, 'core/update_event.html', {'formset': formset})






class UpdateStudentsView(View):
    def get(self, request):
        queryset = Student.objects.all().order_by('date_of_birth')
        formset = modelformset_factory(Student, form=StudentForm , extra=0)

        formset = formset(queryset=queryset)
        return render(request, 'update_student.html', {'formset': formset})

    def post(self, request):
        formset = modelformset_factory(Student, form=StudentForm)
        formset = formset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect('students_update')
        return render(request, 'update_student.html', {'formset': formset})
    
    


def dashboard(request):

    boys_events_qs = Event.objects.filter(is_boys_event=True).order_by('name')
    girls_events_qs = Event.objects.filter(is_boys_event=False).order_by('name')
    recent_event_winners = EventParticipation.objects.filter(position=1)
    top_performers = Student.objects.all().order_by('-points')


    ordered_houses = enumerate(House.objects.all().order_by('-points'), start=1)
    context = {
        'houses': ordered_houses,
        'boys_events': boys_events_qs,
        'girls_events': girls_events_qs,
        'recent_events': recent_event_winners,
        'top_performers': top_performers,
    }

    return render(request, 'core/index.html', context)


def CreateMultipleParticipationsView(request, age_group, gender, event_name):

    event = Event.objects.get(name=event_name)  
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
        return redirect('edit_data') 

def register_participants(request, age_group, gender, event_name):

    if request.method == 'GET':
        match age_group:
            case "u14":
                eligible_participants = Student.objects.filter()
            case "u15":
                pass
            case "u16":
                pass
            case "u17":
                pass
            case "u18":
                pass
            case "u20":
                pass
            case "open":
                pass


        return render(request, 'core/register_participants.html', context = context)

