from rest_framework.serializers import ModelSerializer

from .models import AthleticEvent, EventParticipation, Participant

class EventParticipationSerializer(ModelSerializer):
    class Meta:
        model = EventParticipation
        fields = '__all__'

class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'