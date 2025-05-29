from rest_framework import serializers
from .models import Board, List, Card, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'card', 'author', 'content', 'created_at']


class CardSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)
    members = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        many=True,
        required=False,         
        allow_null=True         
    )

    class Meta:
        model = Card
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ['id', 'board', 'name', 'order', 'created_at', 'cards']


class BoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    lists = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'visibility', 'members', 'created_at', 'lists', 'is_archived']

