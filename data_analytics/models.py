from django.db import models

class AnalyticsData(models.Model):
    date = models.DateField(auto_now_add=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    new_patients = models.IntegerField()
    # Добавьте другие поля для ваших аналитических данных

    class Meta:
        verbose_name = "Аналитические данные"
        verbose_name_plural = "Аналитические данные"

    def __str__(self):
        return f"Аналитика за {self.date}"