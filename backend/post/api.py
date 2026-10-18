import re

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from post.models import Post, Trend
from account.models import FriendshipRequest, User
from account.serializers import FriendshipRequestSerializer, UserSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, PostDetailSerializer, TrendSerializer
from .forms import PostForm, PostAttachmentForm

# Create your views here.


@api_view(['GET'])
def post_list(request):
    posts = []
    trend = request.GET.get('trend', '')
    if (trend):
        posts = Post.objects.visible_to(request.user).filter(body__iregex=rf'\B#{re.escape(trend)}\b')
    else:
        user_friends = request.user.friends.all()
        query = Q()

        # Add user's friends in the query
        for friend in user_friends:
            query |= Q(created_by=friend)
        # Add request user in the query
        query |= Q(created_by=request.user)

        posts = Post.objects.visible_to(request.user).filter(query)

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
        'created_by': request.user.id,
        'is_private': data.get('is_private'),
    })

    # Validate the image before saving anything, so an invalid file
    # doesn't leave a post without its image behind
    attachment_form = None
    if request.FILES.get('image'):
        attachment_form = PostAttachmentForm(files=request.FILES)
        if not attachment_form.is_valid():
            return JsonResponse({'error': attachment_form.errors.as_json()}, status=400)

    if form.is_valid():
        post = form.save()
        user.posts_count += 1
        user.save()
        if attachment_form:
            user.post_attachments.create(image=attachment_form.cleaned_data['image'], post=post)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        message = form.errors.as_json()
        return JsonResponse({'error': message}, status=400)


@api_view(['GET'])
def post_list_profile(request, id):
    user = get_object_or_404(User, pk=id)
    posts = Post.objects.visible_to(request.user).filter(created_by=user)

    for post in posts:
        post.post_liked = post.likes.filter(created_by=request.user).exists()

    paginator = PageNumberPagination()
    paginator.page_size = 10
    posts = paginator.paginate_queryset(posts, request)

    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    check_if_friends = user.friends.filter(id=request.user.id).exists()
    friendshipRequest = ''

    if not check_if_friends:
        friends = False
        check_if_freqeust_sent_received = FriendshipRequest.objects.filter(
            created_for=request.user, created_by=user, status=FriendshipRequest.SENT)
        check_if_freqeust_sent_sent = FriendshipRequest.objects.filter(
            created_for=user, created_by=request.user, status=FriendshipRequest.SENT)
        if check_if_freqeust_sent_received.exists():
            friendshipRequest = check_if_freqeust_sent_received[0]
        elif check_if_freqeust_sent_sent.exists():
            friendshipRequest = check_if_freqeust_sent_sent[0]
    else:
        friends = True

    return paginator.get_paginated_response({
        "posts": post_serializer.data,
        "user": user_serializer.data,
        "friends": friends,
        "friendship_request": FriendshipRequestSerializer(friendshipRequest).data
    })


@api_view(['POST'])
def post_like(request, post_id):
    post = get_object_or_404(Post.objects.visible_to(request.user), id=post_id)
    result = post.add_like(request.user)
    return JsonResponse({'message': result})


@api_view(['GET'])
def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.visible_to(request.user), id=post_id)
    post.post_liked = post.likes.filter(created_by=request.user).exists()
    return JsonResponse({'post': PostDetailSerializer(post).data}, safe=False)


@api_view(['POST'])
def post_create_comment(request, post_id):
    post = get_object_or_404(Post.objects.visible_to(request.user), id=post_id)
    comment = str(request.data.get('comment') or '').strip()
    if not comment:
        return JsonResponse({'message': 'comment is empty'}, status=400)

    result = post.add_comment(request.user, comment)

    return JsonResponse({'message': result}, safe=False)


@api_view(['DELETE'])
def post_delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post.objects.visible_to(request.user), id=post_id)

    if not post.delete_comment(request.user, comment_id):
        return JsonResponse({'message': 'no comment found!'}, status=404)

    return JsonResponse({'message': 'comment deleted successfully'})


@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    return JsonResponse(TrendSerializer(trends, many=True).data, safe=False)


@api_view(['DELETE'])
def post_delete(request, post_id):
    post = get_object_or_404(Post, created_by=request.user, id=post_id)
    post.delete_post(user=request.user)
    return JsonResponse({'message': 'Post deleted'})


@api_view(['POST'])
def report_post(request, post_id):
    post = get_object_or_404(Post.objects.visible_to(request.user), id=post_id)
    report = str(request.data.get('reportText') or '').strip()
    if not report:
        return JsonResponse({'message': 'report is empty'}, status=400)

    post.reports.create(created_by=request.user, report=report)
    return JsonResponse({'message': 'Post reported'})
