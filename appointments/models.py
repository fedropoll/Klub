from django.db import models

TIME_SLOTS = [
    ('08:00-09:00', '08:00-09:00'),
    ('09:00-10:00', '09:00-10:00'),
    ('10:00-11:00', '10:00-11:00'),
    ('11:00-12:00', '11:00-12:00'),
    ('12:00-13:00', '12:00-13:00'),
    ('13:00-14:00', '13:00-14:00'),
    ('14:00-15:00', '14:00-15:00'),
    ('15:00-16:00', '15:00-16:00'),
    ('16:00-17:00', '16:00-17:00'),
    ('17:00-18:00', '17:00-18:00'),
]

class Appointment(models.Model):
    patient = models.ForeignKey(
        'listpatients.Patient',
        on_delete=models.CASCADE,
        related_name='calendar_appointments',
        verbose_name='Пациент'
    )
    doctor = models.ForeignKey(
        'listdoctors.Doctor',
        on_delete=models.CASCADE,
        related_name='calendar_appointments',
        verbose_name='Доктор'
    )
    date = models.DateField(verbose_name='Дата')
    time_slot = models.CharField(
        max_length=20,
        choices=TIME_SLOTS,
        verbose_name='Временной слот'
    )

    def __str__(self):
        return f"Приём пациента {self.patient.full_name} у доктора {self.doctor.name} на {self.date} в {self.time_slot}"

    class Meta:
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"
        unique_together = ('doctor', 'date', 'time_slot')