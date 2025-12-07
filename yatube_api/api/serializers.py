from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Post, Group, Comment, Follow
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = "__all__"
        model = Comment


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ("user", "following")

    def validate(self, data):
        if self.context["request"].user == data["following"]:
            raise serializers.ValidationError("Нельзя подписаться на самого себя")
        return data

    def create(self, validated_data):
        return Follow.objects.create(
            user=self.context["request"].user, **validated_data
        )
