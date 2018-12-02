from django.urls import path
from core.apps import CoreConfig
from core import views


app_name = CoreConfig.name


urlpatterns = [
    path('request',
         views.AnalysisViewSet.as_view({'post': 'common_request'}),
         name='analysis_request'),
]