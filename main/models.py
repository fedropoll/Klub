from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from listdoctors.models import Doctor

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    ROLES = (
        ('patient', 'Пациент'),
        ('doctor', 'Врач'),
        ('admin', 'Администратор'),
        ('director', 'Директор'),
        ('staff', 'Персонал'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    role = models.CharField(max_length=10, choices=ROLES, default='patient')

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"


class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [('M','Мужской'),('F','Женский'),('O','Другой')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name or self.user.email


class EmailVerificationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > (self.created_at + timedelta(minutes=10))

    def __str__(self):
        return f"Код для {self.user.email}: {self.code}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled','Запланировано'),
        ('completed','Завершено'),
        ('cancelled','Отменено'),
        ('rescheduled','Перенесено'),
    ]
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('listdoctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments')
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='service_appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        doctor_name = "N/A"
        if self.doctor:
            try:
                doctor_name = self.doctor.user_profile.user.get_full_name() or self.doctor.user_profile.user.email
            except AttributeError:
                pass
        return f"Запись {self.client.full_name or self.client.user.email} с Dr. {doctor_name} на {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending','Ожидает оплаты'),
        ('paid','Оплачено'),
        ('refunded','Возвращено'),
        ('failed','Неуспешно'),
    ]
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='payments')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Оплата {self.amount} от {self.client.full_name or self.client.user.email} ({self.get_status_display()})"


@receiver(post_save, sender=CustomUser)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        ClientProfile.objects.create(user=instance)
        if instance.user_profile.role == 'doctor':
            Doctor.objects.create(user_profile=instance.user_profile)
