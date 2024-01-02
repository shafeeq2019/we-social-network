from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api.signup, name='signup'),
    path('friends/request/<uuid:id>', api.send_friendship_request, name='send_friendship_request'),
     path('friends/', api.friends, name='friends')
]