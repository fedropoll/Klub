from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, UserProfile, ClientProfile, EmailVerificationCode, Appointment, Payment
from listdoctors.models import Doctor
from services.models import Service
from listdoctors.serializers import DoctorSerializer
from services.serializers import ServiceSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

User = get_user_model()


# ------------------- JWT для ролей -------------------
class RoleTokenObtainPairSerializer(TokenObtainPairSerializer):
    allowed_role = None  # Переопределяем в наследниках

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Пользователь не найден")
        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль")
        if not hasattr(user, 'user_profile'):
            raise serializers.ValidationError("Профиль пользователя не найден")

        if self.allowed_role and getattr(user.user_profile, 'role', '').lower() != self.allowed_role.lower():
            raise serializers.ValidationError(f"Этот токен доступен только для роли {self.allowed_role}")

        data = super().validate(attrs)
        data['role'] = user.user_profile.role
        return data


class AdminTokenObtainPairSerializer(RoleTokenObtainPairSerializer):
    allowed_role = 'admin'


class DirectorTokenObtainPairSerializer(RoleTokenObtainPairSerializer):
    allowed_role = 'director'


class DoctorTokenObtainPairSerializer(RoleTokenObtainPairSerializer):
    allowed_role = 'doctor'


class ClientTokenObtainPairSerializer(RoleTokenObtainPairSerializer):
    allowed_role = 'patient'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email уже зарегистрирован."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)

        # Создаём профили безопасно
        UserProfile.objects.get_or_create(user=user, defaults={'role': 'patient'})
        ClientProfile.objects.get_or_create(user=user)

        return user



# ------------------- Профили -------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['full_name', 'phone', 'birth_date', 'gender', 'address', 'about', 'is_email_verified']
        read_only_fields = ['is_email_verified']


class CurrentUserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    client_profile = ClientProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'last_login',
            'user_profile', 'client_profile'
        )


# ------------------- Записи -------------------
class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'service', 'start_time', 'end_time', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'start_time', 'end_time', 'notes']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Время окончания должно быть позже времени начала.")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'client_profile'):
            validated_data['client'] = request.user.client_profile
        else:
            raise serializers.ValidationError("Только аутентифицированные пользователи с профилем клиента могут создавать записи.")
        return super().create(validated_data)


# ------------------- Оплата -------------------
class PaymentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'service', 'amount', 'payment_date', 'status', 'transaction_id', 'appointment']
        read_only_fields = ['id', 'payment_date', 'status', 'transaction_id', 'amount', 'appointment']


# ------------------- Email verification -------------------
class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6)
