from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from post.models import Post
from account.models import User
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

    return JsonResponse({
        "posts": post_serializer.data,
        "user": user_serializer.data},
        safe=False)
