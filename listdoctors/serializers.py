from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        # fields = '__all__'  # вместо этого:
        fields = ['id', 'name', 'email', 'tags', 'clients', 'birth_date', 'address', 'phone', 'gender']
