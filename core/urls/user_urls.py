from django.urls import path
from core.apps import CoreConfig
from core import views


app_name = CoreConfig.name

urlpatterns = [
    path('list', views.UserViewSet.as_view({'get': 'list'}), name='list'),
    path('register', views.UserViewSet.as_view({'post': 'registration'}),
         name='register'),
    path('logout', views.UserViewSet.as_view({'get': 'logout'}),
         name='logout'),
    path('login', views.UserViewSet.as_view({'post': 'login'}), name='login')
]
