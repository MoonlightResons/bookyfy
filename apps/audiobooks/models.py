from django.db import models
from apps.users.models import ContentMaker, MyUser


class Genre(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Audiobooks(models.Model):
    title = models.CharField(max_length=255, null=False)
    short_description = models.TextField(max_length=1200)
    audio_book = models.FileField(upload_to='audio', blank=False)
    book_img = models.ImageField(upload_to='book_img', blank=False)
    created_by = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name='created_audiobooks')
    genres = models.ManyToManyField(Genre, related_name='audio')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audiobooks, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class AudioComment(models.Model):
    content = models.TextField(max_length=570, blank=False)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audiobooks, on_delete=models.CASCADE, related_name='audio', null=False)


class PendingAudiobooks(models.Model):
    title = models.CharField(max_length=255, null=False)
    short_description = models.TextField(max_length=1200)
    audio_book = models.FileField(upload_to='audio', blank=False)
    book_img = models.ImageField(upload_to='book_img', blank=False)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='created_pending')
    genres = models.ManyToManyField(Genre, related_name='pending_audio')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


