from django.http import JsonResponse
# To override the settings in setting.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm
from .models import FriendshipRequest, User
from .serializers import UserSerializer, FriendshipRequestSerializer


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email
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
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
    else:
        message = form.errors.as_json()
    print(message)

    return JsonResponse({'message': message})


@api_view(['get'])
def friends(request, id):
    requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
    user = User.objects.get(pk=id)
    
    return JsonResponse({'friends': UserSerializer(user.friends, many=True).data,
                         'user': UserSerializer(user).data,
                         'requests': FriendshipRequestSerializer(requests, many=True).data},
                        safe=False)


@api_view(['POST'])
def send_friendship_request(request, id):

    user = User.objects.get(pk=id)
    friendship_request = FriendshipRequest(
        created_for=user, created_by=request.user)
    friendship_request.save()

    return JsonResponse({'message': "friendship request created"})

@api_view(['POST'])
def handle_request(request, friendshipRequestId, status):
    
    user = request.user
    
    friendshipRequestest = FriendshipRequest.objects.get(id=friendshipRequestId)
    friendshipRequestest.status = status
    friendshipRequestest.save()
    
    # add the user to friends list
    user.friends.add(friendshipRequestest.created_by)
    user.save()
    
    return JsonResponse({'message': "friendship request updated"})