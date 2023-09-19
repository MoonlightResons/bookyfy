from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions, status
from .serializer import UserSerializer, MyTokenObtainPairSerializer
from .permissions import AnnonPermission, IsAccountOwner


@api_view(['GET', 'POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Если это GET-запрос, отобразите HTML-шаблон регистрации
        return render(request, 'registration.html')


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer])
def profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response({'user': user, 'serializer': serializer}, template_name='profile.html')

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': user, 'serializer': serializer}, template_name='profile.html')
        return Response({'user': user, 'serializer': serializer}, template_name='profile.html')

    elif request.method == 'DELETE':
        if user.id == request.user.id:
            user.delete()
            return Response({'message': 'Пользователь успешно удален.'})
        else:
            return Response({'message': 'У вас нет разрешения на удаление этого пользователя.'}, status=403)

    return Response({'user': user}, template_name='profile.html')
