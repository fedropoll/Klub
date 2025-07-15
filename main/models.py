from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('patient', 'Пациент'),
        ('derector', 'Директор'),
        ('stamatolog', 'Стоматолог'),
        ('radiologist', 'Рентгенолог'),
        ('paediatrician', 'Педиатр'),
        ('surgeon', 'Хирург'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=150, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
