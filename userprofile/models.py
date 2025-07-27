from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )

    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('director', 'Директор'),
        ('dentist', 'Стоматолог'),
        ('radiologist', 'Рентгенолог'),
        ('paediatrician', 'Педиатр'),
        ('surgeon', 'Хирург'),
        ('patient', 'Пациент'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    # Поле email удалено, так как оно уже есть в модели User
    experience = models.PositiveIntegerField(
        verbose_name="Опыт работы (лет)",
        blank=True, # Позволяет оставлять поле пустым
        null=True # Позволяет хранить пустое значение в базе данных
    )
    address = models.CharField(max_length=255, verbose_name="Адрес")
    status = models.CharField(max_length=100, choices=ROLE_CHOICES, verbose_name="Роль")
    about = models.TextField(verbose_name="О себе", blank=True)

    def __str__(self):
        return self.full_name