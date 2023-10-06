from .models import Book, PendingBook, BasketItem, BookComment
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = '__all__'
