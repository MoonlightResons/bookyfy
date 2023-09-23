import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import DefaultUser, Seller


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
        password = attrs['password']
        password2 = attrs['password2']

        # Проверка на совпадение паролей
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        # Валидация пароля с помощью Django's validate_password
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        # Проверка на наличие цифр, латинских букв и специальных символов в пароле
        if not (re.search(r'\d', password) and re.search(r'[a-zA-Z]', password) and re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', password)):
            raise serializers.ValidationError({'password': 'Password must contain at least one digit, one letter, and one special character.'})

        return attrs

    def create(self, validated_data):
        user = DefaultUser(
            username=validated_data['username'],
            email=validated_data['email'],
            avatar_img=validated_data.get('avatar_img', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


