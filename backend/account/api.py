from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# To override the settings in setting.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.conf import settings
from .forms import SignupForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from .models import FriendshipRequest, User
from notification.models import Notification
from .serializers import UserSerializer, PrivateUserSerializer, FriendshipRequestSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar_link': request.user.avatar_link()
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2')
    })

    if form.is_valid():
        user = form.save()
        # Temporary
        user.is_active = True
        user.save()

        url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'
        send_mail(
            "Please verify your email",
            f"The url for activating your accout is: {url}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    else:
        message = form.errors.as_json()
    print(message)

    return JsonResponse({'message': message})


@api_view(['get'])
def friends(request, id):
    requests = []
    user = get_object_or_404(User, pk=id)
    if user == request.user:
        requests = FriendshipRequest.objects.filter(
            created_for=user, status=FriendshipRequest.SENT)

    return JsonResponse({'friends': UserSerializer(user.friends, many=True).data,
                         'user': UserSerializer(user).data,
                         'requests': FriendshipRequestSerializer(requests, many=True).data},
                        safe=False)


@api_view(['POST', 'DELETE'])
def send_or_delete_friendship_request(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    user = request.user
    is_friend = user.friends.filter(id=friend.id).exists()

    if request.method == "POST":
        if friend == user:
            return JsonResponse({'message': "you can't send a friendship request to yourself"}, status=400)
        if is_friend:
            return JsonResponse({'message': "you are already friends"}, status=400)

        check1 = FriendshipRequest.objects.filter(
            created_for=user, created_by=friend, status=FriendshipRequest.SENT)
        check2 = FriendshipRequest.objects.filter(
            created_for=friend, created_by=user, status=FriendshipRequest.SENT)

        if not check1 and not check2:
            friendship_request = FriendshipRequest(
                created_for=friend, created_by=user)
            friendship_request.save()
            Notification.objects.create_notification(
                created_for=friend, created_by=user, type_of_notification=Notification.NEWFRIENDREQUEST)

            return JsonResponse(FriendshipRequestSerializer(friendship_request).data, safe=False)
        else:
            return JsonResponse({'message': "friendship request already sent"})
    elif request.method == "DELETE":
        if not is_friend:
            return JsonResponse({'message': "you are not friends"}, status=400)

        user.friends.remove(friend)
        user.update_friends_count()
        friend.update_friends_count()
        return JsonResponse({'message': "friendship removed"})


@api_view(['POST'])
def handle_request(request, friend_id, request_id):
    user = request.user
    friend = get_object_or_404(User, id=friend_id)
    status = request.data.get('status')

    # The sender can cancel a request, the receiver can accept or reject it
    if status == FriendshipRequest.CANCELED:
        created_for, created_by = friend, user
    elif status in (FriendshipRequest.ACCEPTED, FriendshipRequest.REJECTED):
        created_for, created_by = user, friend
    else:
        return JsonResponse({'message': 'invalid status'}, status=400)

    friendshipRequest = get_object_or_404(
        FriendshipRequest, id=request_id, created_for=created_for,
        created_by=created_by, status=FriendshipRequest.SENT)

    friendshipRequest.status = status
    friendshipRequest.save()

    # add the user to friends list
    if status == FriendshipRequest.ACCEPTED:
        user.friends.add(friend)
        user.update_friends_count()
        friend.update_friends_count()

        # send a notification
        Notification.objects.create_notification(
            created_for=friend, created_by=user, type_of_notification=Notification.ACCEPTEDFRIENDREQUEST)

        # delete from the suggestion list
        user.people_you_may_know.remove(friend)
        friend.people_you_may_know.remove(user)

    elif status == FriendshipRequest.REJECTED:
        Notification.objects.create_notification(
            created_for=friend, created_by=user, type_of_notification=Notification.REJECTEDFRIENDREQUEST)

    return JsonResponse(FriendshipRequestSerializer(friendshipRequest).data, safe=False)


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    data = request.data
    response = {'message': 'success'}

    form = EditProfileForm(data, request.FILES, instance=user)

    if form.is_valid():
        user = form.save()
        updated_user = User.objects.get(id=user.id)
        response['updated_user'] = PrivateUserSerializer(updated_user).data
        logger.info(f"Profile edited successfully for user {user.id}")
    else:
        response['message'] = form.errors.as_json()
        logger.error(f"Error editing profile for user {
                     user.id}: {response['message']}")

    return JsonResponse(response)


@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(request.user, request.data)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        return JsonResponse({"message": "success"})
    else:
        message = form.errors.as_json()
        print(message)
        return JsonResponse({'message': message}, safe=False)


@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(
        request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)
