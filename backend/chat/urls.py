from . import api
from django.urls import include, path

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:user_id>/', api.message_controller, name='messages')
]