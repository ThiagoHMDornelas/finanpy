from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import LandingPageView, DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include('users.urls')),
    path('contas/', include('accounts.urls')),
    path('categorias/', include('categories.urls')),
    path('transacoes/', include('transactions.urls')),
    path('perfil/', include('profiles.urls')),
    path('', include('ai.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
