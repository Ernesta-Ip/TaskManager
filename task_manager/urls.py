from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from tasks.views import (
    GoogleLogin,
    GoogleLoginCallback,
    LoginPage,
    BoardViewSet,
    ListViewSet,
    CardViewSet,
    CommentViewSet,
    SkipAuthRedirectView,
)
from tasks.views import SocialAccountInfoView

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='boards')
router.register(r'lists', ListViewSet, basename='list')
router.register(r'cards', CardViewSet, basename='card')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path("", LoginPage.as_view(), name="home"),
    path("login/", LoginPage.as_view(), name="login"),
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),  
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/pages/", include("allauth.urls")),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),  # /register/
    path('api/v1/social-accounts/', SocialAccountInfoView.as_view(), name='social-accounts'),
    path("api/v1/skip-auth-redirect/", SkipAuthRedirectView.as_view(), name="skip_auth_redirect"),
#     path("api/v1/auth/google/", include('allauth.socialaccount.providers.google.urls')),
    # path("api/v1/auth/google/callback/", GoogleLoginCallback.as_view(), name="google_login_callback"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
