from django.urls import path

from ai.views import AIAnalysisDetailView, GenerateAnalysisView

app_name = 'ai'

urlpatterns = [
    path('analise/gerar/', GenerateAnalysisView.as_view(), name='generate_analysis'),
    path(
        'analise/<int:pk>/',
        AIAnalysisDetailView.as_view(),
        name='analysis_detail',
    ),
]
