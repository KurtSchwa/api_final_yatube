from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# Добавляем импорт пагинации и стандартного пермишена
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, mixins, permissions, viewsets
# Импортируем IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Комбинируем права: 
    # IsAuthenticatedOrReadOnly - чтобы анонимы могли читать, но не писать (решает ошибку 401).
    # IsAuthorOrReadOnly - чтобы редактировать мог только автор.
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination # <--- Включаем пагинацию
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("group",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # Для групп права можно оставить стандартные или IsAuthenticatedOrReadOnly, 
    # но так как это ReadOnlyModelViewSet, запись и так запрещена.


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # То же самое: запрещаем анонимам POST запросы
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        serializer.save(
            author=self.request.user,
            post=post
        )


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        