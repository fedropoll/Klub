from rest_framework import serializers
from .models import Branch
from safe.services.models import Service  # Проверяем, что Service существует в services/models.py
from safe.main.models import UserProfile, ClientProfile  # Проверяем, что модели существуют в main/models.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

class BranchSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(read_only=True)
    director_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='director', write_only=True, required=False, allow_null=True)
    photo_url = serializers.ImageField(source='photo', read_only=True)

    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'phone_number', 'email', 'is_active', 'director', 'director_id', 'photo', 'photo_url')
        read_only_fields = ('director', 'photo_url')

class ServiceSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'price', 'duration_minutes', 'is_active', 'branch', 'branch_name', 'photo')
        read_only_fields = ('id', 'branch_name')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной.")
        return value

    def validate_duration_minutes(self, value):
        if value < 15:
            raise serializers.ValidationError("Длительность должна быть не менее 15 минут.")
        return value