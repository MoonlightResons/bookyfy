from django.db import models
from apps.users.models import MyUser, DefaultUser


class Book(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1200, null=False)
    author = models.CharField(max_length=255, null=False)
    price = models.IntegerField(null=False)
    book_img = models.ImageField(upload_to='rbook_img', null=False)
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PendingBook(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1200, null=False)
    author = models.CharField(max_length=255, null=False)
    price = models.IntegerField(null=False)
    book_img = models.ImageField(upload_to='rbook_img')
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} {self.book.title}(s) in {self.basket}'
