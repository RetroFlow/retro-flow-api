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
        url(r'^boards/', views.BoardViewSet.as_view(actions={'get': 'list', 'post': 'create'})),

        url(r'^profiles/', views.UserProfileViewSet.as_view(actions={'get': 'list'})),
        url(r'^profile/', views.UserProfileViewSet.as_view(actions={'get': 'retrieve',  'patch': 'partial_update'})),

]

team_router = routers.DefaultRouter()
team_router.register(r'teams', views.TeamViewSet, base_name='teams')

members_router = routers.NestedDefaultRouter(team_router, r'teams', lookup='team')
members_router.register('members', views.TeamMembersViewSet, base_name='members')

urlpatterns += team_router.urls
urlpatterns += members_router.urls