from django.urls import path
from django.views.generic import TemplateView

app_name = 'transactions'

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/coming_soon.html'), name='list'),
]