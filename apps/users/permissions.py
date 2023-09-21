from rest_framework import permissions


class AnnonPermission(permissions.BasePermission):
    message = 'You are arledy authenticated'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanModifyUserProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        if request.user and request.user.is_authenticated:
            # Проверяем, имеет ли пользователь права на DELETE и UPDATE
            if request.method in ['DELETE', 'PUT']:
                return request.user.id == view.kwargs.get('pk')  # Проверяем, что пользователь может изменить свой профиль
            return True  # Для других методов разрешение предоставляется

        return False