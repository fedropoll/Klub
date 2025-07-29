from django import forms
from .models import CustomUser, UserProfile

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="E-mail", required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )
        UserProfile.objects.create(user=user, role='patient')
        return user
