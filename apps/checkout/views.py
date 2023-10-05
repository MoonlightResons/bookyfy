from django.db import transaction
from django.shortcuts import render
import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.books.models import BasketItem
from rest_framework.permissions import IsAuthenticated

stripe.api_key = settings.STRIPE_SECRET_KEY

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL


class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Получите все предметы BasketItem для залогиненного пользователя
        basket_items = BasketItem.objects.filter(basket__user=user)

        line_items = []
        total_amount = 0  # Общая сумма заказа в центах

        for basket_item in basket_items:
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': basket_item.book.title,
                    },
                    'unit_amount': int(basket_item.book.price * 100 * basket_item.quantity),
                },
                'quantity': 1
            }
            total_amount += line_item['price_data']['unit_amount']
            line_items.append(line_item)

        try:
            with transaction.atomic():
                for basket_item in basket_items:
                    basket_item.delete()

                checkout_session = stripe.checkout.Session.create(
                    line_items=line_items,
                    mode='payment',
                    success_url=FRONTEND_CHECKOUT_SUCCESS_URL,
                    cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
                )

            return Response({'checkout_url': checkout_session.url, 'total_amount': total_amount / 100.0},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def success_view(request):
    return render(request, 'success.html')


def cancel_view(request):
    return render(request, 'cancel.html')
