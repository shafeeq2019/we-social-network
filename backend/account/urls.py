from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api.signup, name='signup'),
    path('editprofile/', api.edit_profile, name='edit_profile'),
    path('editpassword/', api.edit_password, name='edit_password'),
    path('friends/<uuid:friend_id>/request/', api.send_or_delete_friendship_request, name='send_or_delete_friendship_request'),
    path('friends/<uuid:friend_id>/request/<uuid:request_id>/', api.handle_request, name='process_friendship_request'),
    path('friends/<uuid:id>/', api.friends, name='friends'),
    path('friends/suggested/', api.my_friendship_suggestions, name='my_friendship_suggestions'),
]