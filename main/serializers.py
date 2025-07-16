from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, ClientProfile

# 👉 Для сотрудников
class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже используется")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data['email']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        UserProfile.objects.create(user=user, role=role)
        return user


# 👉 Для клиентов
class ClientRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        from django.core.mail import send_mail
        import random

        full_name = validated_data['full_name']
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=False
        )

        code = str(random.randint(1000, 9999))

        ClientProfile.objects.create(
            user=user,
            full_name=full_name,
            confirmation_code=code
        )

        send_mail(
            subject="Ваш код подтверждения",
            message=f"Ваш код: {code}",
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=True
        )

        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
