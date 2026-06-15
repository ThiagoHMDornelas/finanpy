from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'
    verbose_name = 'Análise IA'

    def ready(self):
        import ai.signals  # noqa: F401