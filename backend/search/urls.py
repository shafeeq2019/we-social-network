from . import api
from django.urls import include, path

urlpatterns = [
    path('', api.search, name='search'),
]
