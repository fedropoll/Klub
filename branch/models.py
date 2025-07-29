from django.db import models
from main.models import CustomUser

class Branch(models.Model):
    name = models.CharField("Название филиала", max_length=255)
    address = models.CharField("Адрес", max_length=255)
    director = models.ForeignKey(CustomUser, verbose_name="Директор", on_delete=models.PROTECT, related_name='branches')
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"
