from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from apps.audiobooks.models import Genre, Audiobooks
from apps.users.models import MyUser, DefaultUser


class Rate(models.Model):
    rate = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return str(self.rate)

class Book(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1200, null=False)
    author = models.CharField(max_length=255, null=False)
    price = models.IntegerField(null=False)
    book_img = models.ImageField(upload_to='rbook_img', null=False)
    genres = models.ManyToManyField(Genre)
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def update_rating(self):
        avg_rating = self.comments.aggregate(Avg('comment_rate__rate'))['comment_rate__rate__avg']
        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)
        else:
            avg_rating = 0.00

        self.rating = avg_rating
        self.save()

    def __str__(self):
        return self.title


class BookComment(models.Model):
    comment_content = models.TextField(null=False)
    comment_rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books', null=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f"Comment by {self.comment_author} on {self.product}"


class PendingBook(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1200, null=False)
    author = models.CharField(max_length=255, null=False)
    price = models.IntegerField(null=False)
    book_img = models.ImageField(upload_to='rbook_img')
    seller = models.ForeignKey(MyUser, on_delete=models.PROTECT)
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
