from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('director', 'Директор'),
        ('dentist', 'Стоматолог'),
        ('radiologist', 'Рентгенолог'),
        ('paediatrician', 'Педиатр'),
        ('surgeon', 'Хирург'),
        ('patient', 'Пациент'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} ({self.role})"

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    confirmation_code = models.CharField(max_length=6)
    is_email_verified = models.BooleanField(default=False)
    code_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
# models.py
from django.contrib.auth.models import User
from django.db import models
import uuid
from datetime import datetime, timedelta

class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_codes')
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return self.created_at < datetime.now() - timedelta(hours=24)
