import mimetypes
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, action
from rest_framework import permissions, status
from apps.users.permissions import IsContentMaker, IsAudiobookOwner
from .models import Audiobooks
from .sirializer import AudioBookSerializer
from apps.users.models import ContentMaker
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@permission_classes([IsContentMaker])
@renderer_classes([TemplateHTMLRenderer])
def add_audiobook(request):
    if request.method == 'GET':
        serializer = AudioBookSerializer()
        return Response({'serializer': serializer}, template_name='audio_book_create.html')

    elif request.method == "POST":
        title = request.data.get('title')
        short_description = request.data.get("short_description")
        audio_book = request.data.get("audio_book")
        book_img = request.data.get("book_img")

        if request.user.is_Contentmaker:
            author = request.user

        audiobook = Audiobooks.objects.create(
            title=title,
            short_description=short_description,
            audio_book=audio_book,
            book_img=book_img,
            created_by=author
        )

        messages.success(request, "Аудиокнига успешно добавлена.")
        return redirect('profile')


@api_view(['GET'])
def stream_audio(request, audiobook_id):
    try:
        audiobook = Audiobooks.objects.get(pk=audiobook_id)
    except Audiobooks.DoesNotExist:
        return Response({"message": "Аудиокнига не найдена"}, status=status.HTTP_404_NOT_FOUND)

    audio_file_path = os.path.join(settings.MEDIA_ROOT, str(audiobook.audio_book))

    if not os.path.exists(audio_file_path):
        return Response({"message": "Файл аудиокниги не найден"}, status=status.HTTP_404_NOT_FOUND)

    with open(audio_file_path, 'rb') as audio_file:
        response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = f'inline; filename="{audiobook.audio_book.name}"'
        return response


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsAudiobookOwner])
@renderer_classes([TemplateHTMLRenderer])
def audiobook_detail(request, audiobook_id):
    try:
        audiobook = Audiobooks.objects.get(pk=audiobook_id)
    except Audiobooks.DoesNotExist:
        return Response({'detail': 'Audiobook not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AudioBookSerializer(audiobook)
        return Response({'serializer': serializer, 'audiobook': audiobook}, template_name='audiobook_detail.html')

    elif request.method == "PUT":
        if request.user != request.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        short_description = request.data.get("short_description")
        audio_book = request.data.get("audio_book")
        book_img = request.data.get("book_img")

        audiobook.title = title
        audiobook.short_description = short_description
        if book_img:
            audiobook.book = book_img

        if audio_book:
            audiobook.audio_book = audio_book

        audiobook.save()

        messages.success(request, "Аудиокнига успешно обновлена.")
        return redirect('audiobook_detail', audiobook_id=audiobook_id)

    elif request.method == "DELETE":
        if request.user != audiobook.author:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        audiobook.delete()
        return redirect('profile')