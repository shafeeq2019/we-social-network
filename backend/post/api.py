from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from post.models import Post, Trend
from account.models import FriendshipRequest, User
from account.serializers import UserSerializer
from django.db.models import Q

from .serializers import PostSerializer, PostDetailSerializer, TrendSerializer
from .forms import PostForm

# Create your views here.


@api_view(['GET'])
def post_list(request):
    posts = []
    trend = request.GET.get('trend', '')
    if (trend):
        posts = Post.objects.filter(body__iregex=f'\B#{trend}')
    else:
        user_friends = request.user.friends.all()
        query = Q()

        # Add user's friends in the query
        for friend in user_friends:
            query |= Q(created_by=friend)
        # Add request user in the query
        query |= Q(created_by=request.user)

        posts = Post.objects.filter(query)

    for post in posts:
        post.post_liked = post.likes.filter(created_by=request.user).exists()

    paginator = PageNumberPagination()
    paginator.page_size = 10
    posts = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(posts, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def post_create(request):
    data = request.data
    user = request.user

    form = PostForm({
        'body': data.get('body'),
        'created_by': request.user.id
    })

    if form.is_valid():
        post = form.save()
        user.posts_count += 1
        user.save()
        if data.get('image'):
            user.post_attachments.create(image=data.get('image'), post=post)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        message = form.errors.as_json()
        return JsonResponse({'error': message})


@api_view(['GET'])
def post_list_profile(request, id):
    posts = Post.objects.filter(created_by_id=id)
    user = User.objects.get(pk=id)

    for post in posts:
        post.post_liked = post.likes.filter(created_by=request.user).exists()

    paginator = PageNumberPagination()
    paginator.page_size = 10
    posts = paginator.paginate_queryset(posts, request)

    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    check_if_friends = user.friends.filter(id=request.user.id).exists()
    can_send_friendship_request = False

    if not check_if_friends:
        check_if_freqeust_sent_1 = FriendshipRequest.objects.filter(
            created_for=request.user, created_by=user, status=FriendshipRequest.SENT).exists()
        check_if_freqeust_sent_2 = FriendshipRequest.objects.filter(
            created_for=user, created_by=request.user, status=FriendshipRequest.SENT).exists()
        if not check_if_freqeust_sent_1 and not check_if_freqeust_sent_2:
            can_send_friendship_request = True

    return paginator.get_paginated_response({
        "posts": post_serializer.data,
        "user": user_serializer.data,
        "can_send_friendship_request": can_send_friendship_request},)


@api_view(['POST'])
def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    result = post.add_like(request.user)
    return JsonResponse({'message': result})


@api_view(['GET'])
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    post.post_liked = post.likes.filter(created_by=request.user).exists()
    return JsonResponse({'post': PostDetailSerializer(post).data}, safe=False)


@api_view(['POST'])
def post_create_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    comment = request.data.get('comment')
    result = post.add_comment(request.user, comment)

    print(comment)
    return JsonResponse({'message': result}, safe=False)


@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    return JsonResponse(TrendSerializer(trends, many=True).data, safe=False)


@api_view(['DELETE'])
def post_delete(request, post_id):
    post = Post.objects.get(created_by = request.user, id = post_id)
    post.delete();
    
    return JsonResponse({'message': 'Post deleted'})
