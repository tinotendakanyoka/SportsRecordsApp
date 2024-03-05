from django import forms
from django.forms import ModelForm, BaseFormSet

from .models import Student, Event, EventParticipation
from django.forms import modelformset_factory

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__' 
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input
        }




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'  



class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = '__all__'  



# create a form 
class GeeksForm(forms.Form): 
	title = forms.CharField() 
	description = forms.CharField() 



# Define the fields you want to include
fields = ['title', 'description']

# Create the formset factory
GeeksFormFormSet = modelformset_factory(GeeksForm, form=GeeksForm, fields=fields)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     event = cleaned_data.get('event')
    #     student = cleaned_data.get('student')
    #     # position = cleaned_data.get('position')
    #     # laptime_or_distance = cleaned_data.get('laptime_or_distance')
        
        
    #     # Check for duplicate participation
    #     if EventParticipation.objects.filter(event=event, student=student).exists():
    #         raise forms.ValidationError("This student is already participating in this event.")

    #     return cleaned_data

class EventParticipationFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:

            # Dynamically set querysets based on form data or other logic:
            if 'event' in self.data:  # Check if 'event' field exists in submitted data
                selected_event_id = self.data['event']
                form.fields['student'].queryset = Student.objects.filter(allowed_events__id=selected_event_id)  # Filter students based on the selected event
    
            # Provide appropriate options for other fields:
            form.fields['position'].choices = [(i, f"Position {i+1}") for i in range(1, 11)]  # Options for position (1-10)
            form.fields['laptime_or_distance'].choices = [('', '-- Select --'), ('Time', 'Time'), ('Distance', 'Distance')]  # Options for laptime or distance, including an empty first option
    
            # Optional: Consider adding default values using `initial` parameter:
            form.initial = {'position': 0, 'laptime_or_distance': ''}  # Set defaults for position and laptime/distance

        for form in self.forms:
            form.fields['event'].queryset = Event.objects.all()  # Set queryset for event field (unchanged)


# class EventParticipationFormSet(BaseFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for form in self.forms:
#             form.fields['event'].queryset = Event.objects.all()
#             form.fields['student'].queryset = Student.objects.all()
#             form.fields['position'].queryset = [0]
#             form.fields['laptime_or_distance'].queryset = ['']

