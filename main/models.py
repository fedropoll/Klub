from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('patient', 'Пациент'),
        ('director', 'Директор'),
        ('dentist', 'Стоматолог'),
        ('radiologist', 'Рентгенолог'),
        ('paediatrician', 'Педиатр'),
        ('surgeon', 'Хирург'),
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
