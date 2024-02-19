from . import api
from django.urls import include, path

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('<uuid:post_id>/like/', api.post_like, name='post_like'),
    path('<uuid:post_id>/detail/', api.post_detail, name='post_like'),
    path('<uuid:post_id>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<uuid:post_id>/comment/<uuid:comment_id>/', api.post_delete_comment, name='post_delete_comment'),
    path('<uuid:post_id>/', api.post_delete, name='post_delete'),
    path('<uuid:post_id>/report/', api.report_post, name='report_post'),
    path('trends/', api.get_trends, name='get_trends'),
]
