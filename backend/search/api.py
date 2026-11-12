from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer

SEARCH_LIMIT = 50


@api_view(['POST'])
def search(request):
    data = request.data
    query = str(data.get('query') or '').strip()
    users = []
    posts = []

    if query:
        # Capped so a short query like "a" can't load the whole database
        users = User.objects.filter(name__icontains=query).order_by('name')[:SEARCH_LIMIT]
        posts = Post.objects.visible_to(request.user).with_details(
            request.user).filter(body__icontains=query)[:SEARCH_LIMIT]

    return JsonResponse(
        {
            "users": UserSerializer(users, many=True).data,
            "posts": PostSerializer(posts, many=True).data
        }, safe=False)
