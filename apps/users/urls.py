from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    user_registration,
    contentmaker_registration,
    profile,
    get_user_profile,
)

urlpatterns = [
    path('register/', user_registration, name='user-registration'),
    path('content/register/', contentmaker_registration, name='contentmaker-registration'),
    path('profile/', profile, name='profile'),
    path('<int:user_id>/', get_user_profile, name='another-profile'),
    path('content/<int:user_id>/', get_user_profile, name='another-profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]


