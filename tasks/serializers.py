from rest_framework import serializers
from .models import Board, List, Card, Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.serializers import UserDetailsSerializer

User = get_user_model()

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('provider', 'uid', 'extra_data')

class UserSerializer(UserDetailsSerializer):
    social_accounts = SocialAccountSerializer(many=True, read_only=True, source='socialaccount_set')

    class Meta:
        model = User
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'social_accounts'] #+ ('social_accounts',)
        fields = UserDetailsSerializer.Meta.fields + ('social_accounts',)

    def get_profile_picture(self, user):
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            return social_account.extra_data.get('profile_picture')
        except SocialAccount.DoesNotExist:
            return None
        
    def get_social_account_info(user):
        try:
            social_account = SocialAccount.objects.get(user=user)
            return {
                'provider': social_account.provider,
                'uid': social_account.uid,
                'extra_data': social_account.extra_data,  # includes name, email, picture, etc.
            }
        except SocialAccount.DoesNotExist:
            return None

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'card', 'author', 'text', 'created_at', 'edited_at']


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
    created_by = serializers.SerializerMethodField()
    lists = ListSerializer(many=True, read_only=True)
    member_email_list = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'name', 'visibility', 'member_emails', 'member_email_list', 'created_by',
            'created_at', 'lists', 'is_archived', 'order']
        read_only_fields = ['created_by']

    def get_member_email_list(self, obj):
        return obj.get_member_email_list()
    
    def get_created_by(self, obj):
        user = obj.created_by
        return {
            "id": user.id,
            "email": user.email,
            "full_name": f"{user.first_name} {user.last_name}".strip() or user.username
        }

