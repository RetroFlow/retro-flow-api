from django.conf.urls import url
from rest_framework_nested import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r'boards', views.BoardViewSet, base_name='board')
# router.register(r'profiles', views.UserProfileViewSet, base_name='profile')

urlpatterns = [
        url(r'^default_settings/', views.BoardSettingsApiView.as_view()),

        url(r'^boards/(?P<pk>(\d+))/start_new_sprint', views.BoardViewSet.as_view(actions={'get': 'start_new_sprint'})),
        url(r'^boards/(?P<pk>(\d+))/', views.BoardViewSet.as_view(actions={'delete': 'destroy'})),
        url(r'^board/(?P<pk>(\d+))/', views.DeepBoardViewSet.as_view(actions={'get': 'retrieve'})),
        url(r'^boards/', views.BoardViewSet.as_view(actions={'get': 'list', 'post': 'create'})),

        url(r'^profiles/', views.UserProfileViewSet.as_view(actions={'get': 'list'})),
        url(r'^profile/', views.UserProfileViewSet.as_view(actions={'get': 'retrieve',  'patch': 'partial_update'})),
        url(r'^vote/', views.VoteViewSet.as_view(actions={'post': 'create'})),
        url(r'^vote/(?P<pk>(\d+))/', views.VoteViewSet.as_view(actions={'delete': 'destroy'})),

]

team_router = routers.DefaultRouter()
team_router.register(r'teams', views.TeamViewSet, base_name='teams')

members_router = routers.NestedDefaultRouter(team_router, r'teams', lookup='team')
members_router.register('members', views.TeamMembersViewSet, base_name='members')
group_router = routers.NestedDefaultRouter(team_router, r'teams', lookup='team')
group_router.register('groups', views.GroupsViewSet, base_name='groups')

item_router = routers.DefaultRouter()
item_router.register(r'items', views.PlainItemViewSet, base_name='items')

comment_router = routers.NestedDefaultRouter(item_router, r'items', lookup='item')
comment_router.register('comments', views.CommentsViewSet, base_name='comments')

urlpatterns += team_router.urls
urlpatterns += members_router.urls
urlpatterns += item_router.urls
urlpatterns += comment_router.urls
urlpatterns += group_router.urls
