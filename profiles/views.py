from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from .models import Profile
from .forms import ProfileUpdateForm, CustomPasswordChangeForm

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profiles/profile_form.html'
    success_url = reverse_lazy('profiles:detail')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'profiles/password_change.html'
    success_url = reverse_lazy('profiles:detail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Senha alterada com sucesso!')
        return super().form_valid(form)
