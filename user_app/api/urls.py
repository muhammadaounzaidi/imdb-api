from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
import rest_framework.decorators
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns=[
    # path('login/',obtain_auth_token,name='login'),
    path('register/', register_user, name='register'),
    path('logout/',logout_view, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]