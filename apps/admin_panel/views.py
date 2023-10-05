from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.audiobooks.models import PendingAudiobooks, Audiobooks
from apps.audiobooks.serializer import PendingAudioSerializer, AudioBookSerializer
from apps.books.models import Book, PendingBook
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import serializers
from apps.books.serializer import PendingBookSerializer, BookSerializer
from apps.users.models import ContentMaker, MyUser
from apps.users.permissions import IsStaff
from apps.users.serializer import UserSerializer, MyUserSerializer


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
                    audio_book=pending_audio.audio_book,
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


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsStaff])
@csrf_exempt
def admin_user_control(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    csrf_token = get_token(request)
    audiobooks = Audiobooks.objects.filter(created_by=user)
    books = Book.objects.filter(seller=user)

    if request.method == 'GET':
        user_serializer = MyUserSerializer(user)
        audiobooks_serializer = AudioBookSerializer(audiobooks, many=True)
        books_serializer = BookSerializer(books, many=True)
        show_about_field = user.is_Contentmaker
        return Response({'user': user_serializer.data,
                         'audiobooks': audiobooks_serializer.data, 'books': books_serializer.data,
                         'csrf_token': csrf_token, 'show_about_field': show_about_field,
                         'user_id': user_id})

    if request.method == 'PUT':
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

        return redirect('admin-user-control', user_id=user_id)

    if request.method == 'DELETE':
        user.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsStaff])
def admin_users_list(request):
    users = MyUser.objects.all()
    serializer = MyUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsStaff])
def admin_audio_control(request, audiobook_id):
    try:
        audiobook = Audiobooks.objects.get(pk=audiobook_id)
    except Audiobooks.DoesNotExist:
        return Response({'detail': 'Audiobook not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AudioBookSerializer(audiobook)
        return Response({'audiobook': serializer.data})

    elif request.method == "PUT":
        title = request.data.get('title')
        short_description = request.data.get("short_description")
        audio_book = request.data.get("audio_book")
        book_img = request.data.get("book_img")

        if title:
            audiobook.title = title
        if short_description:
            audiobook.short_description = short_description
        if book_img:
            audiobook.book = book_img
        if audio_book:
            audiobook.audio_book = audio_book

        audiobook.save()

        messages.success(request, "Аудиокнига успешно обновлена.")
        return redirect('admin-audio-control', audiobook_id=audiobook_id)

    elif request.method == "DELETE":
        audiobook.delete()
        return redirect('admin-audio-control', audiobook_id=audiobook_id)


@api_view(["GET"])
@permission_classes([IsStaff])
def admin_audio_list(request):
    audio = Audiobooks.objects.all()
    serializer = AudioBookSerializer(audio, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsStaff])
def admin_book_control(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return Response({'book': serializer.data})

    elif request.method == "PUT":
        title = request.data.get('title')
        description = request.data.get("description")
        author = request.data.get("author")
        price = request.data.get("price")
        book_img = request.data.get("book_img")

        if title:
            book.title = title
        if description:
            book.description = description
        if author:
            book.author = author
        if price:
            book.price = price
        if book_img:
            book.book_img = book_img
        if book:
            book.book = book

        book.save()

        messages.success(request, "Книга успешно обновлена.")
        return redirect('admin-book-control', book_id=book_id)

    elif request.method == "DELETE":
        book.delete()
        return redirect('admin-book-control', book_id=book_id)


@api_view(["GET"])
@permission_classes([IsStaff])
def admin_book_list(request):
    book = Book.objects.all()
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data)