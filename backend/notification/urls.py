from . import api
from django.urls import include, path

urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:id>/', api.read_notification, name='read_notification'),
]
