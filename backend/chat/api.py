from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from account.models import User

from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer


@api_view(['GET'])
def conversation_list(request):
    request_user = request.user
    conversations = request_user.conversations.filter()  # messages__isnull=False
    return JsonResponse({"conversations": ConversationSerializer(conversations, many=True).data}, safe=False)


@api_view(['GET', 'DELETE', 'POST'])
def message_controller(request, user_id):
    request_user = request.user
    message_user = get_object_or_404(User, id=user_id)

    if request.method == "GET":
        try:
            conversation = request_user.conversations.get(
                users__in=[message_user])
        except ObjectDoesNotExist:
            conversation = request_user.conversations.create()
            conversation.users.add(message_user)

        return JsonResponse({"conversation": ConversationDetailSerializer(conversation).data}, safe=False)

    conversation = get_object_or_404(
        request_user.conversations, users__in=[message_user])

    if request.method == "DELETE":
        conversation.delete()
        return JsonResponse({'message': 'Conversation deleted'})
    elif request.method == "POST":
        conversation_2 = message_user.conversations.filter(
            users__in=[request_user])

        conversation_1_message = conversation.messages.create(message=request.data.get(
            'message'), created_by=request_user, sent_to=message_user)

        # If the receiving user has deleted the conversation:
        if not conversation_2.exists():
            conversation = message_user.conversations.create()
            conversation.users.add(request_user)

        conversation_2_message = conversation_2[0].messages.create(message=request.data.get(
            'message'), created_by=request_user, sent_to=message_user)

        return JsonResponse({"message": ConversationMessageSerializer(conversation_1_message).data}, safe=False)

