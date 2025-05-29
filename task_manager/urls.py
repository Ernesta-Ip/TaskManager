from django.contrib import admin
from django.urls import path, include
from tasks.views import login_redirect_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')), 
    path('accounts/', include('allauth.urls')), 
    path('auth/', include('rest_framework.urls')),
    # path('login-redirect/', login_redirect_view, name='login-redirect'),
]
