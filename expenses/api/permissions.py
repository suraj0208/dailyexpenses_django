from rest_framework import permissions


class Permissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, expense):
        return expense.expense_owner == request.user
