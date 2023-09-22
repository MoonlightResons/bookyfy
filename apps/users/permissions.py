from rest_framework import permissions


class AnnonPermission(permissions.BasePermission):
    message = 'You are arledy authenticated'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsContentMaker(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_Contentmaker


class IsAudiobookOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
