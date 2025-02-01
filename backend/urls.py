from rest_framework_simplejwt.views import TokenRefreshView
from project_app.views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register/', Signup, name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('', include('project_app.urls')),
]
