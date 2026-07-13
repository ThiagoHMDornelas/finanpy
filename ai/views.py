from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import DetailView

from ai.models import AIAnalysis


class AIAnalysisDetailView(LoginRequiredMixin, DetailView):
    model = AIAnalysis
    template_name = 'ai/analysis_detail.html'
    context_object_name = 'analysis'

    def get_queryset(self):
        return AIAnalysis.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404
        return obj
