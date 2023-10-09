from django.contrib import admin
from .models import Audiobooks, PendingAudiobooks, Genre, AudioComment, Likes

admin.site.register(Audiobooks)
admin.site.register(PendingAudiobooks)
admin.site.register(Genre)
admin.site.register(AudioComment)
admin.site.register(Likes)
