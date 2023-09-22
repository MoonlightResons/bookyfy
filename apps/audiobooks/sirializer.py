from rest_framework import serializers
from .models import Audiobooks


class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audiobooks
        fields = '__all__'
