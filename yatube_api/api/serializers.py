from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator # Импорт валидатора

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        # Важно: делаем поле post доступным только для чтения,
        # чтобы его нельзя было изменить при редактировании комментария
        read_only_fields = ("post", "author") 


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ("user", "following")
        # Добавляем валидатор, чтобы нельзя было подписаться дважды на одного и того же
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following")
            )
        ]

    def validate(self, data):
        # Получаем пользователя из контекста запроса
        request_user = self.context["request"].user
        
        # Проверяем подписку на самого себя
        if request_user == data["following"]:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        return data
    