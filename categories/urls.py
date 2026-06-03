from django.urls import path
from django.views.generic import TemplateView

app_name = 'categories'

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/coming_soon.html'), name='list'),
]