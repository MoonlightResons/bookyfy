from apps.books.models import Book
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from apps.books.models import Book, PendingBook, Basket, BasketItem, BookComment, Rate
from apps.books.serializer import BookSerializer, BasketItemSerializer, CommentSerializer
from apps.users.permissions import IsBookSeller, IsOwnerOfBasket
from apps.audiobooks.models import Genre


@api_view(['GET', 'POST'])
@permission_classes([])
@renderer_classes([TemplateHTMLRenderer])
def add_book(request):
    genres = Genre.objects.all()
    if request.method == 'GET':
        serializer = BookSerializer()
        return Response({'serializer': serializer, "genres": genres}, template_name='book_create.html')

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
                seller=seller,
            )

            genre_ids = request.data.getlist('genres')
            pending_book.genres.set(genre_ids)

            messages.success(request, "Книга успешно отправлена на одобрение.")

            # Включите форму в контекст ответа
            serializer = BookSerializer()
            return Response({'serializer': serializer, "genres": genres, 'detail': 'Книга успешно отправлена на одобрение.'}, template_name='book_create.html')

        else:
            messages.error(request, "Вы должны быть продавцом, чтобы добавить книгу.")
            return redirect('profile')


@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, IsBookSeller])
@renderer_classes([TemplateHTMLRenderer])
def book_detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book    not found'}, template_name='book_detail.html', status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BookSerializer(book)
        genres = book.genres.all()
        comments = BookComment.objects.filter(book=book)  # Получаем все комментарии для данной книги
        print("Genres:", genres)

        return Response({'book': serializer.data, 'comments': comments, "genres": genres}, template_name='book_detail.html')

    elif request.method == "PUT":
        if request.user != book.seller:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

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

        book.save()

        messages.success(request, "Книга успешно обновлена.")
        return redirect('book-detail', book_id=book_id)

    elif request.method == "POST":
        comment_content = request.data.get('comment_content')
        comment_rate_value = request.data.get('comment_rate')

        if comment_rate_value is not None:
            comment_rate_value = int(comment_rate_value)
        else:
            return Response({'detail': 'Invalid comment rate value.'}, status=status.HTTP_400_BAD_REQUEST)

        comment_author = request.user
        comment_rate, created = Rate.objects.get_or_create(rate=comment_rate_value)

        new_comment = BookComment.objects.create(
            comment_content=comment_content,
            comment_rate=comment_rate,
            comment_author=comment_author,
            book=book
        )

        messages.success(request, "Комментарий успешно добавлен.")
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


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id, book_id):
    try:
        comment = BookComment.objects.get(pk=comment_id)
    except BookComment.DoesNotExist:
        return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        if request.user != comment.comment_author:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        comment_content = request.data.get('comment_content')
        comment_rate_value = request.data.get('comment_rate')
        if comment_rate_value is not None:
            comment_rate_value = int(comment_rate_value)
        else:
            return Response({'detail': 'Invalid comment rate value.'}, status=status.HTTP_400_BAD_REQUEST)
        comment_rate, created = Rate.objects.get_or_create(rate=comment_rate_value)

        if comment_content:
            comment.comment_content = comment_content
        if comment_rate:
            comment.comment_rate = comment_rate

        comment.save()

        return Response({'detail': 'Комментарий успешно обновлен.'}, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        if request.user != comment.comment_author:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            comment.delete()
            return Response({'detail': 'Комментарий успешно удален.'}, status=status.HTTP_200_OK)


# def homepage(request):
#     all_books = Book.objects.all()
#
#     data = [
#         {'title': book.title, 'author': book.author, 'genres': book.genres}
#         for book in all_books
#     ]
#     query = request.GET.get('q')
#     genre_filter = request.GET.get('genres')
#
#     if query:
#         filtered_books = all_books.filter(Q(title__icontains=query) | Q(author__icontains=query))
#     elif genre_filter:
#         filtered_books = all_books.filter(genre=genre_filter)
#     else:
#         filtered_books = all_books
#
#     # Получите текущего пользователя (здесь предполагается, что вы используете аутентификацию пользователей Django)
#     current_user = request.user
#
#     # Получите данные о взаимодействиях текущего пользователя с книгами
#     user_interactions = UserInteraction.objects.filter(user=current_user)
#
#     # Соберите оценки пользователя для каждой книги в виде списка
#     user_ratings = {interaction.book: interaction.rating for interaction in user_interactions}
#
#     # Проверка на наличие оценок пользователя
#     if user_ratings:
#         # Создайте список текстовых описаний книг
#         book_descriptions = [f"{book.title} {book.author}" for book in user_ratings.keys()]
#
#         # Инициализация и обучение TfidfVectorizer
#         tfidf_vectorizer = TfidfVectorizer()
#         tfidf_matrix = tfidf_vectorizer.fit_transform([f"{item['title']} {item['author']}" for item in data])
#
#         # Обучите модель KNN для рекомендаций на основе матрицы TF-IDF
#         knn_recommend_books = NearestNeighbors(n_neighbors=5)  # Пример: 5 ближайших соседей
#         knn_recommend_books.fit(tfidf_matrix)
#
#         # Используйте модель KNN для предсказания рекомендованных книг
#         user_tfidf_vector = tfidf_vectorizer.transform(book_descriptions)
#         recommended_books_indices = knn_recommend_books.kneighbors(user_tfidf_vector, n_neighbors=5)
#         recommended_books_indices = recommended_books_indices[1][0]
#
#         # Получите рекомендованные книги
#         recommended_books = [data[index] for index in recommended_books_indices]
#     else:
#         # Если у пользователя нет оценок, вы можете предоставить другие рекомендации или сообщение
#         recommended_books = []
#
#     return render(request, 'homepage.html', {'books': filtered_books, 'recommended_books': recommended_books})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def book_list(request):
    book = Book.objects.all()
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data)