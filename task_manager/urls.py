from django.contrib import admin
from django.urls import path, re_path, include
from tasks.views import GoogleLogin, GoogleLoginCallback, LoginPage
from django.conf import settings
from django.conf.urls.static import static
# from tasks.views import login_redirect_view
from tasks.views import BoardViewSet, ListViewSet, CardViewSet, CommentViewSet
# from rest_framework.routers import DefaultRouter

urlpatterns = [
      path("", LoginPage.as_view(), name="home"),
      path('admin/', admin.site.urls),
      # path("auth/login/redirect/", login_redirect_view, name="login_redirect"),
      path("login/", LoginPage.as_view(), name="login"),
      path("api/v1/auth/", include("dj_rest_auth.urls")),
      re_path(r"^api/v1/auth/pages/", include("allauth.urls")),
      # path("api/v1/auth/pages/", include("allauth.urls")),
      path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
      path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
      path("api/v1/auth/google/callback/",GoogleLoginCallback.as_view(), name="google_login_callback"),
#     path('accounts/', include('allauth.urls')), 
#     path('auth/', include('rest_framework.urls')),
#     path('dj-rest-auth/', include('dj_rest_auth.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# router = DefaultRouter()
# router.register(r'boards', BoardViewSet, basename='board')
# router.register(r'lists', ListViewSet)
# router.register(r'cards', CardViewSet)
# router.register(r'comments', CommentViewSet)

# urlpatterns = [
#      path('', include(router.urls)),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)