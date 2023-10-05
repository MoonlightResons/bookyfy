from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from .managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=55, null=False)
    email = models.EmailField('email address', unique=True, null=False)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    is_Seller = models.BooleanField(default=False)
    is_Contentmaker = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'
    
    
class DefaultUser(MyUser):
    avatar_img = models.ImageField(upload_to='avatars', default='default-avatar.jpg', null=True)


class ContentMaker(MyUser):
    avatar_img = models.ImageField(upload_to='avatars', default='default-avatar.jpg', null=True)
    about = models.TextField()


class Seller(MyUser):
    about = models.TextField()
    telephone_number = models.CharField(max_length=255)

