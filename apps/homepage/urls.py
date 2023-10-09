from django.urls import path
from .views import homepage, books

urlpatterns = [
    path('', homepage, name='audio-list-homepage'),
    path('market/', books, name='books-list-homepage'),
]
