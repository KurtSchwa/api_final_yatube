from django.contrib import admin
from .models import Group, Post, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author", "group", "pub_date")
    list_filter = ("author", "group", "pub_date")


admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)
