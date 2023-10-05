from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from apps.books.models import Book, PendingBook, Basket, BasketItem
from apps.books.serializer import BookSerializer, BasketItemSerializer
from apps.users.permissions import IsBookSeller, IsOwnerOfBasket


@api_view(['GET', 'POST'])
@permission_classes([])
@renderer_classes([TemplateHTMLRenderer])
def add_book(request):
    if request.method == 'GET':
        serializer = BookSerializer()
        return Response({'serializer': serializer}, template_name='book_create.html')

    elif request.method == "POST":
        title = request.data.get('title')
        description = request.data.get("description")
        author = request.data.get("author")
        price = request.data.get("price")
        book_img = request.data.get("book_img")

        if request.user.is_Seller:
            seller = request.user

            pending_book = PendingBook.objects.create(
                title=title,
                description=description,
                book_img=book_img,
                author=author,
                price=price,
                seller=seller
            )

            messages.success(request, "Книга успешно отправлена на одобрение.")

            # Включите форму в контекст ответа
            serializer = BookSerializer()
            return Response({'serializer': serializer, 'detail': 'Книга успешно отправлена на одобрение.'}, template_name='book_create.html')

        else:
            messages.error(request, "Вы должны быть продавцом, чтобы добавить книгу.")
            return redirect('profile')


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsBookSeller])
@renderer_classes([TemplateHTMLRenderer])
def book_detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, template_name='book_detail.html', status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return Response({'serializer': serializer.data, 'book': serializer.data}, template_name='book_detail.html')

    elif request.method == "PUT":
        if request.user != request.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN,)

        title = request.data.get('title')
        description = request.data.get("description")
        author = request.data.get("author")
        price = request.data.get("price")
        book_img = request.data.get("book_img")

        book.title = title
        book.description = description
        book.author = author
        book.price = price
        if book_img:
            book.book_img = book_img

        if book:
            book.book = book

        book.save()

        messages.success(request, "Книга успешно обновлена.")
        return redirect('book-detail', book_id=book_id)

    elif request.method == "DELETE":
        if request.user != book.seller:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            book.delete()
            return redirect('profile')


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsOwnerOfBasket])
@renderer_classes([TemplateHTMLRenderer])
def add_book_basket(request):
    user = request.user

    try:
        basket = Basket.objects.get(user=user)
    except Basket.DoesNotExist:
        return Response({'message': 'Корзина не существует'}, status=status.HTTP_404_NOT_FOUND)

    book_id = request.POST.get('book_id')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'message': 'Книга не существует'}, status=status.HTTP_404_NOT_FOUND)

    basket_item, created = BasketItem.objects.get_or_create(basket=basket, book=book)
    serializer = BasketItemSerializer(basket_item)

    if not created:
        basket_item.quantity += 1
        basket_item.save()
        return redirect("basket-items-detail")

    return Response({'message': 'Книга успешно добавлена в корзину'}, template_name='book_detail.html',
                    status=status.HTTP_200_OK)


@api_view(['GET', "DELETE"])
@permission_classes([IsAuthenticated, IsOwnerOfBasket])
def basket_items_delete(request, item_id):
    try:
        basket_item = BasketItem.objects.get(id=item_id, basket__user=request.user)
    except BasketItem.DoesNotExist:
        return Response({'detail': 'Basket item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized_data = BasketItemSerializer(basket_item).data
        return Response({'basket_item': serialized_data}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        basket_item.delete()
        return Response({'detail': 'Basket item deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwnerOfBasket])
def get_basket_items(request):
    user = request.user

    try:
        basket_items = BasketItem.objects.filter(basket__user=user)
    except BasketItem.DoesNotExist:
        return Response({'detail': 'Basket items not found'}, status=status.HTTP_404_NOT_FOUND)

    serialized_data = BasketItemSerializer(basket_items, many=True).data
    return Response({'basket_items': serialized_data}, status=status.HTTP_200_OK)





