from .models import Book, PendingBook, BasketItem
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class PendingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingBook
        fields = '__all__'


class BasketItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketItem
        fields = '__all__'

