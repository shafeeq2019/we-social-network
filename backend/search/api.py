from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer


@api_view(['POST'])
def search(request):
    data = request.data
    query = data.get('query')
    query = query.strip()
    users = []
    posts = []

    if query:
        users = User.objects.filter(name__icontains=query)
        posts = Post.objects.filter(body__icontains=query)

        for post in posts:
            post.post_liked = post.likes.filter(
                created_by=request.user).exists()

    return JsonResponse(
        {
            "users": UserSerializer(users, many=True).data,
            "posts": PostSerializer(posts, many=True).data
        }, safe=False)
