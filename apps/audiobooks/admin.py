from django.contrib import admin
from .models import Audiobooks, PendingAudiobooks, Genre

admin.site.register(Audiobooks)
admin.site.register(PendingAudiobooks)
admin.site.register(Genre)
