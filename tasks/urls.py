from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BoardViewSet, ListViewSet, CardViewSet, CommentViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'lists', ListViewSet)
router.register(r'cards', CardViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
     path('', include(router.urls)),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
