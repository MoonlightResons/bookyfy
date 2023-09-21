from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, action
from rest_framework import permissions, status
from .serializer import UserSerializer, MyTokenObtainPairSerializer
from .permissions import AnnonPermission, IsAccountOwner, CanModifyUserProfile
from .models import DefaultUser
from django.contrib import messages


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


from django.contrib.auth import authenticate

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer])
def profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response({'user': user, 'serializer': serializer}, template_name='profile.html')

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update':
            # Получите данные из запроса
            username = request.data.get('username')
            email = request.data.get('email')
            avatar_img = request.data.get('avatar_img')

            user.username = username
            user.email = email
            if avatar_img:
                user.avatar_img = avatar_img

                user.save()

                messages.success(request, "Профиль успешно обновлен.")
                return redirect('profile')

        elif action == 'delete':
            user.delete()
            logout(request)
            return redirect('login')  # Вы можете перенаправить пользователя на другую страницу после удаления, если это необходимо

    return Response({'user': user}, template_name='profile.html')




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([TemplateHTMLRenderer])
def get_user_profile(request, user_id):
    try:
        user = DefaultUser.objects.get(pk=user_id)
    except DefaultUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, template_name='another_profile.hmtl')
