from django.urls import path
from core.apps import CoreConfig
from core.search import views

app_name = CoreConfig.name

urlpatterns = [
    path('get', views.SearchViewSet.as_view({'post': 'search'}),
         name='search'),
    path('document', views.SearchViewSet.as_view({'post': 'document'}),
         name='search'),
    path('number_of_links', views.SearchViewSet.as_view({'post': 'number_of_links'}),
         name='number_of_links'),
    path('put', views.SearchViewSet.as_view({'get': 'put'}), name='put'),
]
