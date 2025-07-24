import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.conf import settings

from .models import ClientProfile

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class StaffRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='staff', write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже зарегистрирован.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        UserProfile.objects.create(user=user, role=role)
        return user


from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import ClientProfile
import random

class ClientRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        validate_password(data['password'])
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email уже зарегистрирован.")
        return data

    def create(self, validated_data):
        email = validated_data['email']
        full_name = validated_data['full_name']
        password = validated_data['password']
        code = str(random.randint(1000, 9999))

        user = User.objects.create(
            username=email,
            email=email,
            is_active=False,
        )
        user.set_password(password)
        user.save()

        ClientProfile.objects.create(
            user=user,
            full_name=full_name,
            confirmation_code=code,
            is_email_verified=False,
            code_created_at=timezone.now()
        )

        # Отправка кода подтверждения на почту
        from django.core.mail import send_mail
        from django.conf import settings

        send_mail(
            subject="Код подтверждения для Safe Clinic",
            message=f"Ваш код подтверждения: {code}. Срок действия — 5 минут.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            user = User.objects.get(email=email)
            profile = ClientProfile.objects.get(user=user)
        except (User.DoesNotExist, ClientProfile.DoesNotExist):
            raise serializers.ValidationError("Неверный email или пользователь не существует.")

        if profile.is_email_verified:
            raise serializers.ValidationError("Email уже подтвержден.")

        if profile.code_created_at + timedelta(minutes=5) < timezone.now():
            raise serializers.ValidationError("Код устарел.")

        if profile.confirmation_code != code:
            raise serializers.ValidationError("Неверный код.")

        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        profile = ClientProfile.objects.get(user=user)

        user.is_active = True
        user.save()

        profile.is_email_verified = True
        profile.confirmation_code = ''
        profile.save()
        return user

class ResendVerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            profile = ClientProfile.objects.get(user=user)
            if profile.is_email_verified:
                raise serializers.ValidationError("Email уже подтвержден.")
        except (User.DoesNotExist, ClientProfile.DoesNotExist):
            raise serializers.ValidationError("Пользователь не найден.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        profile = ClientProfile.objects.get(user=user)

        code = str(random.randint(1000, 9999))
        profile.confirmation_code = code
        profile.code_created_at = timezone.now()
        profile.save()

        send_mail(
            subject="Новый код подтверждения",
            message=f"Ваш новый код: {code}. Срок действия — 5 минут.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
