from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Board, List, Card, Comment
from .serializers import BoardSerializer, ListSerializer, CardSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect

def login_redirect_view(request):
    board = Board.objects.filter(is_archived=False).order_by('id').first()
    if board:
        return redirect(f'http://localhost:8080/board/{board.id}')
    return redirect('http://localhost:8080/dashboard')


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Board.objects.all()



class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.AllowAny]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

