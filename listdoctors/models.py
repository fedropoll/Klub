from django.db import models

ROLE_CHOICES = [
    ('implant_surgeon', 'Хирург-имплантолог'),
    ('dentist', 'Стоматолог'),
    ('radiologist', 'Рентгенолог'),
    ('pediatrician', 'Педиатр'),
    ('orthopedic_surgeon', 'Хирург-ортопед'),
    ('surgeon', 'Хирург'),
]

GENDER_CHOICES = [
    ('male', 'Мужской'),
    ('female', 'Женский'),
]

class Doctor(models.Model):
    photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tags = models.CharField(max_length=30, choices=ROLE_CHOICES)  # как просил
    clients = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_tags_display()})"
