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
        return user


