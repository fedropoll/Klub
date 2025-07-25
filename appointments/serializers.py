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
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)

    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor', write_only=True
    )
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='patient', write_only=True
    )

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_id', 'patient_id', 'date', 'time_slot']