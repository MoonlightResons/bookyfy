from rest_framework import serializers
from .models import Audiobooks, PendingAudiobooks, AudioComment


class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audiobooks
        fields = '__all__'


class PendingAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingAudiobooks
        fields = '__all__'


class AudioCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioComment
        fields = '__all__'


