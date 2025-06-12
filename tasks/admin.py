from django.contrib import admin
from .models import Board, List, Card, Comment

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'visibility', 'created_at')
    search_fields = ('name',)


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'order', 'created_at')
    list_filter = ('board',)
    search_fields = ('name',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'due_date', 'created_at')
    list_filter = ('list', 'due_date')
    search_fields = ('title', 'description')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('card', 'author', 'created_at')
    list_filter = ('card', 'author')
    search_fields = ('content',)
