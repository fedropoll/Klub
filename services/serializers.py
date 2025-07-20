from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price',
            'duration_minutes', 'is_active',
            'branch', 'branch_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'branch_name']
