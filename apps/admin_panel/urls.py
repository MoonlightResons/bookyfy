from django.urls import path
from .views import admin_approve_books, admin_approve_audio


urlpatterns = [
    path('approve/book/', admin_approve_books, name='admin-approve-books'),
    path('approve/audio/', admin_approve_audio, name='admin-approve-audio'),
]
