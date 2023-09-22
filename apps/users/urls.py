from django.urls import path
from django.contrib.auth import views as auth_views
# from . import shortcuts
from .views import (
    user_registration,
    profile,
    get_user_profile
)

urlpatterns = [
    path('register/', user_registration, name='user-registration'),
    path('profile/', profile, name='profile'),
    path('profile/<int:user_id>/', get_user_profile, name='another-profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]


