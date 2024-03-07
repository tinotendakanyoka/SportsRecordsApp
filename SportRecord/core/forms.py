from django import forms


from .models import Student, Event, EventParticipation


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



