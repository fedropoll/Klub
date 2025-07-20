from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

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

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название филиала")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email филиала")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_directed_branches', verbose_name="Директор филиала")
    photo = models.ImageField(upload_to='branch_photos/', blank=True, null=True, verbose_name="Фото филиала")

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.name