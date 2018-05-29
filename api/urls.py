from django.conf.urls import url


from .views import BoardSettingsApiView, BoardViewSet

urlpatterns = [
        url(r'^default_settings/', BoardSettingsApiView.as_view()),
        url(r'^boards/', BoardViewSet.as_view(actions={'get': 'list'})),
        url(r'^board/', BoardViewSet.as_view(actions={'post': 'create'})),

]
