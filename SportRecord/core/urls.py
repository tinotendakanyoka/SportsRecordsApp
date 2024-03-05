from django.urls import path
from . import views

urlpatterns = [

    path('events', views.UpdateEventsView.as_view(), name='events_update'),
    path('students', views.UpdateStudentsView.as_view(), name='students_update'),
    path('compete', views.formset_view, name='compete'),
]
