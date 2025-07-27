# appointments/serializers.py

from rest_framework import serializers
from .models import Appointment
from listdoctors.models import Doctor
from listpatients.models import Patient

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'tags']
        ref_name = 'AppointmentDoctorSerializer'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name']
        ref_name = 'AppointmentPatientSerializer'

class AppointmentSerializer(serializers.ModelSerializer):
    # Эти поля только для чтения - используются для вывода данных (GET)
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    # Эти поля только для записи - используются для создания/обновления (POST/PATCH)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='patient', write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor', write_only=True
    )

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_id', 'patient_id', 'date', 'time_slot']
        # Используем extra_kwargs для более явного управления полями
        extra_kwargs = {
            'patient_id': {'write_only': True},
            'doctor_id': {'write_only': True},
        }