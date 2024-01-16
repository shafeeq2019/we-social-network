from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse


@api_view(['GET'])
def notifications(request):
    user = request.user
    received_notifications = user.received_notifications.filter(is_read=False)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    received_notifications = paginator.paginate_queryset(
        received_notifications, request)
    serializer = NotificationSerializer(received_notifications, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def read_notification(request, id):
    user = request.user
    notification = Notification.objects.filter(created_for=user).get(id=id)
    notification.is_read = True
    notification.save()
    return JsonResponse({"message": "test"})
