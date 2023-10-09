from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from apps.audiobooks.models import Audiobooks, Genre
from rest_framework.permissions import IsAuthenticated

from apps.books.models import Book


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def homepage(request):
    genres = Genre.objects.all()

    if request.method == "GET":
        genre_audiobooks = []

        for genre in genres:
            audiobooks = Audiobooks.objects.filter(genres=genre)
            genre_audiobooks.append({'genre': genre, 'audiobooks': audiobooks})

        return render(request, 'homepage.html', {'genre_audiobooks': genre_audiobooks})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def books(request):
    genres = Genre.objects.all()

    if request.method == "GET":
        genre_audiobooks = []

        for genre in genres:
            book = Book.objects.filter(genres=genre)
            genre_audiobooks.append({'genre': genre, 'book': book})

        return render(request, 'market.html', {'genre_audiobooks': genre_audiobooks})







