from django.db import models
from apps.users.models import ContentMaker, MyUser


class Genre(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Audiobooks(models.Model):
    title = models.CharField(max_length=255, null=False)
    short_description = models.TextField(max_length=1200)
    audio_book = models.FileField(upload_to='audio', null=False)
    book_img = models.ImageField(upload_to='book_img', null=False)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='created_audiobooks')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title