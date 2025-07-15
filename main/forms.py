from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(forms.ModelForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, label="Роль", required=True)
    username = forms.CharField(label="Логин", required=True)
    email = forms.EmailField(label="E-mail", required=True)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['role', 'username', 'email', 'password1']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=self.cleaned_data["role"])
        return user