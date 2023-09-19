# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import permissions, status
# from .serializer import UserSerializer, MyTokenObtainPairSerializer
#
#
# @api_view(['GET', 'POST'])
# def user_registration(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             login(request, user)
#             return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
#     else:
#         serializer = UserSerializer()
#
#     return render(request, 'registration.html', {'serializer': serializer})
#
#
# @login_required
# def profile(request):
#     user = request.user
#     return render(request, 'profile.html', {'user': user})
#
