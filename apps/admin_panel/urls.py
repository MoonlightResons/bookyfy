from django.urls import path
from .views import (admin_approve_books, admin_approve_audio, admin_user_control,
                    admin_users_list, admin_audio_control, admin_audio_list,
                    admin_book_control, admin_book_list
                    )


urlpatterns = [
    path('approve/book/', admin_approve_books, name='admin-approve-books'),
    path('approve/audio/', admin_approve_audio, name='admin-approve-audio'),
    path('<int:user_id>/user/control/', admin_user_control, name='admin-user-control'),
    path('<int:audiobook_id>/audio/control/', admin_audio_control, name='admin-audio-control'),
    path('<int:book_id>/book/control/', admin_book_control, name='admin-book-control'),
    path('users/list/', admin_users_list, name='admin-users-list'),
    path('audio/list/', admin_audio_list, name='admin-audio-list'),
    path('book/list/', admin_book_list, name='admin-book-list'),
]
