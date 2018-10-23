from django.urls import path

from core import views


urlpatterns = [
    path('get', views.SearchViewSet.as_view({'post': 'search'})),
    path('put', views.SearchViewSet.as_view({'get': 'put'})),
]
