from . import views
from django.urls import path
from .views import *


urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSession.as_view()),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel')
]