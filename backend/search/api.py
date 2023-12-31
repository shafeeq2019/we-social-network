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

    users = User.objects.filter(name__icontains=query)
    posts = Post.objects.filter(body__icontains=query)

    user_serializer = UserSerializer(users, many=True)
    post_serializer = PostSerializer(posts, show_created_by=True, many=True)
    print('query', query)

    return JsonResponse(
        {
            "users": user_serializer.data,
            "posts": post_serializer.data
        }, safe=False)
