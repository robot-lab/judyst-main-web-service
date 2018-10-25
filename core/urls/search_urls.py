from django.urls import path
from core.apps import CoreConfig
from core import views


app_name = CoreConfig.name

urlpatterns = [
    path('get', views.SearchViewSet.as_view({'post': 'search'}),
         name='search'),
    path('put', views.SearchViewSet.as_view({'get': 'put'}), name='put'),
]
