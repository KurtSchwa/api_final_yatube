from django.contrib.auth import get_user_model
from rest_framework import serializers

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


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ("user", "following")

    def validate(self, data):
        request_user = self.context["request"].user

        if request_user == data["following"]:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        return data

    def create(self, validated_data):
        return Follow.objects.create(
            user=self.context["request"].user,
            **validated_data
        )
