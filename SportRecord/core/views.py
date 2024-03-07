
from django.shortcuts import render, redirect
from django.views import View
from .models import Event, Student, EventParticipation, House
from .forms import EventForm, StudentForm, EventParticipationForm, EventParticipationFormSet, GeeksForm, GeeksFormFormSet
from django.forms import modelformset_factory

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
    
    
def formset_view(request): 
    context ={} 
  
    # creating a formset 
    #GeeksFormSet = modelformset_factory(GeeksForm) 
    formset = GeeksFormFormSet() 
      
    # Add the formset to context dictionary 
    context['formset']= formset 
    return render(request, "home.html", context)

def dashboard(request):


    ordered_houses = enumerate(House.objects.all().order_by('-points'), start=1)
    context = {
        'houses': ordered_houses,
        'range': [1,2,3,4],
    }

    return render(request, 'core/index.html', context)


