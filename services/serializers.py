from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    photo_url = serializers.ImageField(source='photo', read_only=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price', 'duration_minutes',
            'photo', 'photo_url', 'is_active', 'branch', 'branch_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'branch_name', 'photo_url']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной.")
        return value

    def validate_duration_minutes(self, value):
        if value < 15:
            raise serializers.ValidationError("Длительность должна быть не менее 15 минут.")
        return value

    def validate(self, attrs):
        # Убираем возможные попытки изменить даты
        attrs.pop('created_at', None)
        attrs.pop('updated_at', None)
        return attrs
