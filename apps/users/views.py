import re

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, action
from rest_framework import permissions, status
from .serializer import UserSerializer, ContentMakerSerializer
from .permissions import IsNotAuthenticated, IsNotContentMakerAccount
from .models import DefaultUser, MyUser, ContentMaker
from django.contrib import messages
from ..audiobooks.models import Audiobooks
from ..books.models import Book


def is_valid_password(password):
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True


@api_view(["GET", "POST"])
@permission_classes([IsNotAuthenticated])
def user_registration(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if MyUser.objects.filter(email=email).exists():
                return JsonResponse(
                    {"message": "Email is already registered."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not is_valid_password(password):
                return JsonResponse(
                    {"message": "Password is invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return redirect("login")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, "registration.html")


@api_view(["GET", "POST"])
@permission_classes([IsNotAuthenticated])
def contentmaker_registration(request):
    if request.method == "POST":
        serializer = ContentMakerSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if MyUser.objects.filter(email=email).exists():
                return JsonResponse(
                    {"message": "Email is already registered."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not is_valid_password(password):
                return JsonResponse(
                    {"message": "Password is invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return redirect("login")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, "2registration.html")


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer])
@csrf_exempt
def profile(request):
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
                        template_name='profile.html')

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update':
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
        return Response({'user': user}, template_name='profile.html', status=status.HTTP_200_OK, )

    return Response({'user': user}, template_name='profile.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer])
def get_user_profile(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)
    audiobooks = Audiobooks.objects.filter(created_by=user)
    books = Book.objects.filter(seller=user)
    return Response({'user': user, 'audiobooks': audiobooks, 'books': books}, template_name="another_profile.html")
