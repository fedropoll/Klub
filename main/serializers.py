# main/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, ClientProfile # Branch удален
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail
from django.conf import settings

# 👉 Для сотрудников
class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data['email']

        user = User.objects.create_user(
            username=email, # Используем email как username
            email=email,
            password=password,
            is_active=True # Сотрудники активны сразу
        )
        UserProfile.objects.create(user=user, role=role)
        return user


# 👉 Для клиентов: Регистрация и запрос нового кода
class ClientRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован и активен.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        full_name = validated_data['full_name']
        email = validated_data['email']
        password = validated_data['password']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'is_active': False
            }
        )
        if not created:
            user.set_password(password)
            user.save()

        code = str(random.randint(1000, 9999))

        profile, created_profile = ClientProfile.objects.update_or_create(
            user=user,
            defaults={
                'full_name': full_name,
                'confirmation_code': code,
                'is_email_verified': False,
                'code_created_at': timezone.now()
            }
        )

        send_mail(
            subject="Ваш код подтверждения для Safe Clinic",
            message=f"Здравствуйте, {full_name}!\n\nВаш код подтверждения: {code}\n\nЭтот код действителен в течение 5 минут.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return user

# Сериализатор для запроса нового кода (отдельный эндпоинт)
class ResendVerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if not hasattr(user, 'clientprofile') or user.clientprofile.is_email_verified:
                raise serializers.ValidationError("Пользователь не является клиентом или его email уже подтвержден.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)
        profile = user.clientprofile

        code = str(random.randint(1000, 9999))
        profile.confirmation_code = code
        profile.code_created_at = timezone.now()
        profile.is_email_verified = False
        profile.save()

        send_mail(
            subject="Ваш новый код подтверждения для Safe Clinic",
            message=f"Здравствуйте!\n\nВаш новый код подтверждения: {code}\n\nЭтот код действителен в течение 5 минут.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        return user


# Сериализатор для подтверждения email
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        try:
            profile = ClientProfile.objects.get(user=user)
        except ClientProfile.DoesNotExist:
            raise serializers.ValidationError("Профиль клиента не найден.")

        if profile.is_email_verified:
            raise serializers.ValidationError("Email уже подтвержден.")

        if profile.code_created_at + timedelta(minutes=5) < timezone.now():
            raise serializers.ValidationError("Срок действия кода истек. Пожалуйста, запросите новый код.")

        if profile.confirmation_code != code:
            raise serializers.ValidationError("Неверный код подтверждения.")

        return data

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        profile = ClientProfile.objects.get(user=user)
        profile.confirmation_code = ''
        profile.is_email_verified = True
        profile.save()

        return user

