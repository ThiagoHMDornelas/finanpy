from django.urls import path

from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('nova/', CategoryCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', CategoryUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', CategoryDeleteView.as_view(), name='delete'),
]
