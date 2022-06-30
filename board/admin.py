from django.contrib import admin
from .models import Board, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ("contents",)
    list_display = (
        "title",
        "contents",
        "writer",
        "board_name",
        "hits",
        "like_count",
        "write_dttm",
        "update_dttm",
    )
    list_display_links = list_display


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "board",
        "content",
        "writer",
        "created_at",
        "deleted",
    )
    list_display_links = list_display