from rest_framework import serializers
from .models import Appointment
from listdoctors.models import Doctor
from listpatients.models import Patient

from listdoctors.serializers import DoctorSerializer as BaseDoctorSerializer
from listpatients.serializers import PatientSerializer as BasePatientSerializer

class DoctorSerializer(BaseDoctorSerializer):
    class Meta(BaseDoctorSerializer.Meta):
        ref_name = 'AppointmentDoctorSerializer'

class PatientSerializer(BasePatientSerializer):
    class Meta(BasePatientSerializer.Meta):
        ref_name = 'AppointmentPatientSerializer'

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='patient', write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor', write_only=True
    )

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_id', 'patient_id', 'date', 'time_slot']
        extra_kwargs = {
            'patient_id': {'write_only': True},
            'doctor_id': {'write_only': True},
        }