from . import api
from django.urls import include, path

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('<uuid:post_id>/like/', api.post_like, name='post_like'),
]
