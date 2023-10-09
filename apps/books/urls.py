from django.urls import path
from .views import (add_book, book_detail,
                    add_book_basket,
                    basket_items_delete,
                    get_basket_items,
                    comment_detail,
                    book_list)

urlpatterns = [
    path("create/", add_book, name='create-book'),
    path("<int:book_id>/detail/", book_detail, name='book-detail'),
    path('basket/add-book/', add_book_basket, name='basket-add'),
    path('<int:item_id>/basket/items/', basket_items_delete, name='basket-items-delete'),
    path('<int:book_id>/<int:comment_id>/comment/', comment_detail, name='comment-detail'),
    path('basket/', get_basket_items, name='basket-items-detail'),
    path('list/', book_list, name='book-list'),
]
