from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from post.models import Post
from account.models import FriendshipRequest, User
from account.serializers import UserSerializer
from .serializers import PostSerializer
from .forms import PostForm

# Create your views here.


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    # print(posts)
    serializer = PostSerializer(posts, many=True, show_created_by=True)
    # print(serialzer)

    return JsonResponse({'data': serializer.data})


@api_view(['POST'])
def post_create(request):
    data = request.data

    form = PostForm({
        'body': data.get('body'),
        'created_by': request.user.id
    })

    if form.is_valid():
        post = form.save()
        print(post)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        message = form.errors.as_json()
        print(message)
        return JsonResponse({'error': message})


@api_view(['GET'])
def post_list_profile(request, id):
    posts = Post.objects.filter(created_by_id=id)
    user = User.objects.get(pk=id)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    check_if_friends = user.friends.filter(id=request.user.id).exists()
    can_send_friendship_request = False

    if not check_if_friends:
        check_if_freqeust_sent_1 = FriendshipRequest.objects.filter(
            created_for=request.user, created_by=user, status=FriendshipRequest.SENT).exists()
        print("check_if_freqeust_sent_1=", check_if_freqeust_sent_1)
        check_if_freqeust_sent_2 = FriendshipRequest.objects.filter(
            created_for=user, created_by=request.user, status=FriendshipRequest.SENT).exists()
        print("check_if_freqeust_sent_2=", check_if_freqeust_sent_2)
        if not check_if_freqeust_sent_1 and not check_if_freqeust_sent_2:
            can_send_friendship_request = True

    return JsonResponse({
        "posts": post_serializer.data,
        "user": user_serializer.data,
        "can_send_friendship_request": can_send_friendship_request},
        safe=False)
