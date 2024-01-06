from . import api
from django.urls import include, path

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:user_id>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:covnersation_id>/message/', api.conversation_send_message, name='conversation_send_message'),
     path('get-or-create/<uuid:user_id>/', api.conversation_get_or_create, name='conversation_get_or_create'),
]
