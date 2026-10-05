from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
            'placeholder': 'Seu nome',
        }),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
            'placeholder': 'Seu email',
        }),
    )
    avatar = forms.ImageField(
        label='Avatar',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full text-sm text-[#a09cb5] file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-violet-600 file:text-white hover:file:bg-violet-700 cursor-pointer',
            'accept': 'image/*',
        }),
    )

    class Meta:
        model = User
        fields = ('first_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=commit)
        avatar = self.cleaned_data.get('avatar')
        if commit and avatar and hasattr(user, 'profile'):
            user.profile.avatar = avatar
            user.profile.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Senha atual',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
            'placeholder': 'Senha atual',
        }),
    )
    new_password1 = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
            'placeholder': 'Nova senha',
        }),
    )
    new_password2 = forms.CharField(
        label='Confirme a nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg bg-[#0f0d1a] border border-[#2d2754] text-[#f0eef5] placeholder-[#6b6785] focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-all duration-200',
            'placeholder': 'Confirme a nova senha',
        }),
    )
