from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse

from account.models import User
# from account.serializers import UserSerializer
from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer
from .models import Conversation, ConversationMessage


@api_view(['GET'])
def conversation_list(request):
    user = request.user
    conversations = user.conversations.all() #.filter(messages__isnull=False).distinct()
    # conversations2 = Conversation.objects.filter(users__in = [request.user])
    return JsonResponse({"conversations": ConversationSerializer(conversations, many=True).data}, safe=False)


@api_view(['GET'])
def conversation_detail(request, user_id):
    request_user = request.user
    message_user = User.objects.get(id=user_id)
    conversation = Conversation.objects.filter(
        users__in=[request_user]).get(users__in=[message_user])
    return JsonResponse({"conversation": ConversationDetailSerializer(conversation).data}, safe=False)


@api_view(['POST'])
def conversation_send_message(request, covnersation_id):
    user = request.user
    conversation = user.conversations.get(id=covnersation_id)
    sent_to = conversation.users.exclude(id=request.user.id).first()
    conversation_message = conversation.messages.create(message=request.data.get(
        'message'), created_by=user, sent_to=sent_to)

    return JsonResponse({"message": ConversationMessageSerializer(conversation_message).data}, safe=False)


@api_view(['GET'])
def conversation_get_or_create(request, user_id):
    
    request_user = request.user
    message_user = User.objects.get(id=user_id)

    conversations = Conversation.objects.filter(
        users__in=[request_user]).filter(users__in=[message_user])

    if (conversations.exists()):
        conversation = conversations.first()
        print("exists")

    else:
        conversation = request_user.conversations.create()
        conversation.users.add(message_user)

    return JsonResponse(ConversationSerializer(conversation).data, safe=False)
