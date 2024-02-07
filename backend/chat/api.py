from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from account.models import User

from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer


@api_view(['GET'])
def conversation_list(request):
    sender_user = request.user
    conversations = sender_user.conversations.filter()  # messages__isnull=False
    return JsonResponse({"conversations": ConversationSerializer(conversations, many=True).data}, safe=False)


@api_view(['GET', 'DELETE', 'POST'])
def conversation_controller(request, user_id):
    sender_user = request.user
    receiver_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        conversation = sender_user.conversations.filter(
            users__in=[receiver_user])

        if conversation.exists():
            return JsonResponse({'message': 'Conversation already exists'})

        conversation = sender_user.conversations.create()
        conversation.users.add(receiver_user)
        return JsonResponse({"conversation": ConversationDetailSerializer(conversation).data}, safe=False)

    conversation = get_object_or_404(
        sender_user.conversations, users__in=[receiver_user])

    if request.method == "GET":
        return JsonResponse({"conversation": ConversationDetailSerializer(conversation).data}, safe=False)

    elif request.method == "DELETE":
        conversation.delete()
        return JsonResponse({'message': 'Conversation deleted'})


@api_view(['POST'])
def message_controller(request, user_id):
    if request.method == "POST":
        sender_user = request.user
        receiver_user = get_object_or_404(User, id=user_id)
        sender_conversation = get_object_or_404(
            sender_user.conversations, users__in=[receiver_user])

        sender_message = sender_conversation.messages.create(message=request.data.get(
            'message'), created_by=sender_user, sent_to=receiver_user)

        receiver_conversation = receiver_user.conversations.filter(
            users__in=[sender_user])

        # If the receiving user has deleted the conversation:
        if not receiver_conversation.exists():
            receiver_user.conversations.create().users.add(sender_user)

        receiver_message = receiver_conversation[0].messages.create(message=request.data.get(
            'message'), created_by=sender_user, sent_to=receiver_user)

    return JsonResponse({"message": ConversationMessageSerializer(sender_message).data}, safe=False)
