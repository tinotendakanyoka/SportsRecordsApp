from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('events/<int:event_id>/', views.event, name='event'),
    path('event/<int:event_id>/eventparticipation/', views.EventParticipationListCreateAPIView.as_view(), name='eventparticipation-list-create'),
    path('event/<int:event_id>/eligibleparticipants/', views.EligibleParticipantsView.as_view(), name='eligibleparticipants'),
    path('event/<int:event_id>/report', views.report, name='report')
    #path('eventparticipation/<int:pk>/', views.EventParticipationDetail.as_view(), name='eventparticipation-detail'),

    #path('initialize/', views.initialize, name='initialize'),
]
