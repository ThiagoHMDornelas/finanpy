from django.contrib import admin

from ai.models import AIAnalysis


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'period_analyzed', 'model_used', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'analysis_text')
    readonly_fields = ('created_at', 'updated_at', 'tokens_input', 'tokens_output')
    date_hierarchy = 'created_at'
