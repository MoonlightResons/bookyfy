from django.contrib import admin
from apps.books.models import Book, PendingBook, BasketItem, Basket, BookComment, Rate


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [BasketItemInline]
    list_display = ('user', 'created_at')


admin.site.register(Basket, CartAdmin)
admin.site.register(Book)
admin.site.register(PendingBook)
admin.site.register(BookComment)
admin.site.register(Rate)
