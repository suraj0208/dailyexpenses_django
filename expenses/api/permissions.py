from rest_framework import permissions


class Permissions(permissions.BasePermission):
    def has_object_permission(self, request, view, expense):
        return True
