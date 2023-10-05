from rest_framework import serializers
from .models import Audiobooks, PendingAudiobooks


class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audiobooks
        fields = '__all__'


class PendingAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingAudiobooks
        fields = '__all__'


