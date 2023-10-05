from django.urls import path
from .views import admin_approve_books, admin_approve_audio, admin_user_control


urlpatterns = [
    path('approve/book/', admin_approve_books, name='admin-approve-books'),
    path('approve/audio/', admin_approve_audio, name='admin-approve-audio'),
    path('<int:user_id>/user/control/', admin_approve_audio, name='admin-approve-audio'),
]
