from django.conf.urls import url


from .views import BoardSettingsApiView

urlpatterns = [
        url(r'^default_settings/', BoardSettingsApiView.as_view()),

]
