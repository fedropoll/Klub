from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField("Название филиала", max_length=255)
    address = models.CharField("Адрес", max_length=255)
    director = models.ForeignKey(User, verbose_name="Директор", on_delete=models.PROTECT, related_name='branches')
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)

    def __str__(self):
        return self.name
