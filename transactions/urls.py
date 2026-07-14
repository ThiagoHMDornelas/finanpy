from django.urls import path

from .views import TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListView.as_view(), name='list'),
    path('nova/', TransactionCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', TransactionDeleteView.as_view(), name='delete'),
]
