from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.audiobooks.models import PendingAudiobooks, Audiobooks
from apps.audiobooks.serializer import PendingAudioSerializer
from apps.books.models import Book, PendingBook
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import serializers
from apps.books.serializer import PendingBookSerializer
from apps.users.models import ContentMaker
from apps.users.permissions import IsStaff
from apps.users.serializer import UserSerializer


@api_view(['POST', 'GET'])
@permission_classes([IsStaff])
def admin_approve_books(request):
    if request.method == "GET":
        pending_books = PendingBook.objects.all()
        serializer = PendingBookSerializer(pending_books, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        book_id = request.data.get('book_id')
        action = request.data.get('action')

        try:
            pending_book = PendingBook.objects.get(pk=book_id)

            if action == 'approve':
                Book.objects.create(
                    title=pending_book.title,
                    description=pending_book.description,
                    book_img=pending_book.book_img,
                    author=pending_book.author,
                    price=pending_book.price,
                    seller=pending_book.seller,
                    approved=True
                )
                pending_book.delete()
                messages.success(request, "Книга одобрена.")

            elif action == 'reject':
                pending_book.delete()
                messages.success(request, "Книга отклонена и удалена.")

            return Response({'detail': 'Операция выполнена успешно.'})

        except PendingBook.DoesNotExist:
            messages.error(request, "Книга не найдена.")
            return Response({'detail': 'Книга не найдена.'})


@api_view(['POST', 'GET'])
@permission_classes([IsStaff])
def admin_approve_audio(request):
    if request.method == "GET":
        pending_audio = PendingAudiobooks.objects.all()
        serializer = PendingAudioSerializer(pending_audio, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        audio_id = request.data.get('audio_id')
        action = request.data.get('action')

        try:
            pending_audio = PendingAudiobooks.objects.get(pk=audio_id)

            if action == 'approve':
                Audiobooks.objects.create(
                    title=pending_audio.title,
                    short_description=pending_audio.short_description,
                    book_img=pending_audio.book_img,
                    created_by=pending_audio.created_by,
                    approved=True
                )
                pending_audio.delete()
                messages.success(request, "Аудиокнига одобрена.")

            elif action == 'reject':
                pending_audio.delete()
                messages.success(request, "Аудиокнига отклонена и удалена.")

            return Response({'detail': 'Операция выполнена успешно.'})

        except PendingAudiobooks.DoesNotExist:
            messages.error(request, "Аудиокнига не найдена.")
            return Response({'detail': 'Аудиокнига не найдена.'})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsStaff])
@csrf_exempt
def admin_user_control(request, user_id):
    user = request.user
    csrf_token = get_token(request)
    audiobooks = Audiobooks.objects.filter(created_by=user)
    books = Book.objects.filter(seller=user)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        show_about_field = user.is_Contentmaker  # Проверяем, является ли пользователь ContentMaker
        return Response({'user': user, 'serializer': serializer,
                         'audiobooks': audiobooks, 'books': books,
                         'csrf_token': csrf_token, 'show_about_field': show_about_field},
                        user_id=user_id)

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update':
            # Получите данные из запроса
            username = request.data.get('username')
            email = request.data.get('email')
            avatar_img = request.data.get('avatar_img')

            if username:
                user.username = username
            if email:
                user.email = email
            if avatar_img:
                user.avatar_img = avatar_img

            if user.is_Contentmaker:
                about = request.data.get('about')
                if about is not None:
                    user.contentmaker.about = about
                    user.contentmaker.save()

            if username or email or avatar_img or about:
                user.save()

                messages.success(request, "Профиль успешно обновлен.")
            else:
                messages.info(request, "Нет данных для обновления профиля.")

            return redirect('profile')

    if request.method == 'DELETE':
        user.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)






