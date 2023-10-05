from django.contrib import admin
from .models import Audiobooks, PendingAudiobooks

admin.site.register(Audiobooks)
admin.site.register(PendingAudiobooks)
