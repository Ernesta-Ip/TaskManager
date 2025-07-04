from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.db import models
from .models import Board, List, Card, Comment
from .serializers import BoardSerializer, ListSerializer, CardSerializer, CommentSerializer
from django.contrib.auth.models import User

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from urllib.parse import urljoin

import requests
from django.urls import reverse
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from allauth.socialaccount.models import SocialAccount
from .serializers import SocialAccountSerializer

from django.http import FileResponse, Http404
import os

class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )

class SocialAccountInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = SocialAccount.objects.filter(user=request.user)
        serializer = SocialAccountSerializer(accounts, many=True)
        return Response(serializer.data)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = CustomGoogleOAuth2Client # OAuth2Client

   
class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
            
    def get_queryset(self):
            user = self.request.user
            if not user.is_authenticated:
                return Board.objects.filter(visibility='public', is_archived=False)

            return Board.objects.filter(
                models.Q(visibility='public') |
                models.Q(visibility='internal') |
                models.Q(created_by=user.id) |
                models.Q(member_emails__icontains=user.email),
            ).distinct()


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
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})
        return Response(response.json(), status=status.HTTP_200_OK)

class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
    
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = CustomGoogleOAuth2Client

    def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)
            user = request.user
            board = Board.objects.filter(created_by_id=user.id, is_archived=False).order_by('id').first()
            response.data['board_id'] = board.id if board else None
            return response

class SkipAuthRedirectView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        board = Board.objects.filter(visibility='public', is_archived=False).order_by('id').first()
        if board:
            return Response({'board_id': board.id})
        return Response({'board_id': None})

class SecureFileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, filename):
        file_path = os.path.join(settings.MEDIA_ROOT, 'attachments', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        raise Http404("File does not exist")