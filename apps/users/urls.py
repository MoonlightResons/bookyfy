from django.urls import path
from django.contrib.auth import views as auth_views
# from . import shortcuts
from .views import (
    user_registration,
    profile
)

urlpatterns = [
    path('user/register/', user_registration, name='user-registration'),
    path('user/profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]


