from django.urls import include, path

from core import views

urlpatterns = [
    path('', views.UserListView.as_view()),
]