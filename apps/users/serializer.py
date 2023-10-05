import re
from django.contrib.auth.password_validation import validate_password
from django.forms import forms
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import DefaultUser, Seller, ContentMaker
from ..books.models import Basket


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['is_Seller'] = user.is_Seller
        return token


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = DefaultUser
        fields = [
            'id',
            'username',
            'email',
            'avatar_img',
            'password',
            'password2',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match!'}
            )
        return attrs

    def create(self, validated_data):
        user = DefaultUser(
            username=validated_data['username'],
            email=validated_data['email'],
            avatar_img=validated_data.get('avatar_img', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        Basket.objects.create(user=user)
        return user


class ContentMakerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = ContentMaker
        fields = [
            'id',
            'username',
            'email',
            'about',
            'avatar_img',
            'password',
            'password2',
            "is_Contentmaker",
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match!'}
            )
        return attrs

    def create(self, validated_data):
        user = ContentMaker(
            username=validated_data['username'],
            email=validated_data['email'],
            about=validated_data.get('about'),
            avatar_img=validated_data.get('avatar_img', None),
            is_Contentmaker=True  # Установите is_Contentmaker в True для новых пользователей ContentMaker
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



