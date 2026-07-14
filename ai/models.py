from django.conf import settings
from django.db import models


class AIAnalysis(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_analyses',
    )
    analysis_text = models.TextField()
    key_insights = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    period_analyzed = models.CharField(max_length=100)
    model_used = models.CharField(max_length=50, default='gpt-4o-mini')
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    is_latest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'análise IA'
        verbose_name_plural = 'análises IA'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_latest']),
        ]

    def __str__(self):
        return f'{self.user.email} - {self.period_analyzed}'

    def save(self, *args, **kwargs):
        if self.is_latest:
            AIAnalysis.objects.filter(
                user=self.user,
                is_latest=True,
            ).exclude(pk=self.pk).update(is_latest=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_latest_for_user(cls, user_id):
        return cls.objects.filter(user_id=user_id, is_latest=True).first()
