from django.urls import path

from ai.views import AIAnalysisDetailView

app_name = 'ai'

urlpatterns = [
    path(
        'analise/<int:pk>/',
        AIAnalysisDetailView.as_view(),
        name='analysis_detail',
    ),
]
