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

class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  # This is fix for incompatibility between django-allauth==65.3.1 and dj-rest-auth==7.0.1
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


# def login_redirect_view(request):
#      board = Board.objects.filter(is_archived=False).order_by('id').first()
#      if board:
#          return redirect(f'http://localhost:8080/board/{board.id}')
#      return redirect('http://localhost:8080/dashboard')

   
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
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
                models.Q(created_by=user) |
                models.Q(members=user),
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
    permission_classes = [permissions.AllowAny]

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        If you are building a fullstack application (eq. with React app next to Django)
        you can place this endpoint in your frontend application to receive
        the JWT tokens there - and store them in the state
        """

        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        print("token_endpoint_url", token_endpoint_url)
        response = requests.post(url=token_endpoint_url, data={"code": code})
        # print("response: ", response.text)
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