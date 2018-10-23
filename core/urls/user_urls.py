from django.urls import path

from core import views


urlpatterns = [
    path('list', views.UserViewSet.as_view({'get': 'list'})),
    path('register', views.UserViewSet.as_view({'post': 'registration'})),
    path('logout', views.UserViewSet.as_view({'get': 'logout'})),
    path('login', views.UserViewSet.as_view({'post': 'login'}))
]
