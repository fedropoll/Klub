from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название филиала")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email филиала")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_directed_branches', verbose_name="Директор филиала")
    photo = models.ImageField(upload_to='branch_photos/', blank=True, null=True, verbose_name="Фото филиала")

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.name
