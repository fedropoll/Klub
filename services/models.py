from django.db import models
from django.core.validators import MinValueValidator
from branch.models import Branch

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", validators=[MinValueValidator(0)])
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин)", default=30)
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="services", verbose_name="Филиал")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="services", verbose_name="Категория")
    photo = models.ImageField(upload_to='service_photos/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.price}₸)"
