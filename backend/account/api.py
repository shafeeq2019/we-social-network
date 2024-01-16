from django.contrib.auth import authenticate
from django.http import JsonResponse
# To override the settings in setting.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from .models import FriendshipRequest, User
from notification.models import Notification
from .serializers import UserSerializer, FriendshipRequestSerializer
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

        url = f'http://127.0.0.1:8000/activateemail/?email={
            user.email}&id={user.id}'
        send_mail(
            "Please verify your email",
            f"The url for activating your accout is: {url}",
            "noreply@we.com",
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
    user = User.objects.get(pk=id)
    if user == request.user:
        requests = FriendshipRequest.objects.filter(
            created_for=user, status=FriendshipRequest.SENT)

    return JsonResponse({'friends': UserSerializer(user.friends, many=True).data,
                         'user': UserSerializer(user).data,
                         'requests': FriendshipRequestSerializer(requests, many=True).data},
                        safe=False)


@api_view(['POST'])
def send_friendship_request(request, id):
    user = User.objects.get(pk=id)

    check1 = FriendshipRequest.objects.filter(
        created_for=request.user, created_by=user, status=FriendshipRequest.SENT)
    check2 = FriendshipRequest.objects.filter(
        created_for=user, created_by=request.user, status=FriendshipRequest.SENT)

    if not check1 and not check2:
        friendship_request = FriendshipRequest(
            created_for=user, created_by=request.user)
        friendship_request.save()
        Notification.objects.create_notification(
            created_for=user, created_by=request.user, type_of_notification=Notification.NEWFRIENDREQUEST)

        return JsonResponse({'message': "friendship request created"})
    else:
        return JsonResponse({'message': "friendship request already sent"})


@api_view(['POST'])
def handle_request(request, friendshipRequestId, status):

    user = request.user

    friendshipRequestest = FriendshipRequest.objects.get(
        id=friendshipRequestId)
    request_user = friendshipRequestest.created_by
    friendshipRequestest.status = status
    friendshipRequestest.save()

    # add the user to friends list
    if (status == 'accepted'):
        user.friends.add(request_user)
        user.friends_count += 1
        user.save()
        request_user.friends_count += 1
        request_user.save()

        # send a notification
        Notification.objects.create_notification(
            created_for=request_user, created_by=user, type_of_notification=Notification.ACCEPTEDFRIENDREQUEST)
        
        # delete from the suggestion list
        user.people_you_may_know.remove(request_user)
        request_user.people_you_may_know.remove(user)
        
    else:
        Notification.objects.create_notification(
            created_for=request_user, created_by=user, type_of_notification=Notification.REJECTEDFRIENDREQUEST)
         
    return JsonResponse({'message': "friendship request updated"})


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    data = request.data
    response = {'message': 'success'}

    form = EditProfileForm(data, request.FILES, instance=user)

    if form.is_valid():
        user = form.save()
        updated_user = User.objects.get(id=user.id)
        response['updated_user'] = UserSerializer(updated_user).data
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
