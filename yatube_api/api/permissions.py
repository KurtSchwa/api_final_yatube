from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение: только автор может менять или удалять объект,
    остальные только читать."""

    def has_object_permission(self, request, view, obj):
        # Разрешены только безопасные методы (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # На изменение/удаление — только автор
        return obj.author == request.user
