from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('events/<event_name>/<gender>/<age_group>', views.CreateMultipleParticipationsView, name='events'),
    path('students', views.UpdateStudentsView.as_view(), name='students_update'),
]
