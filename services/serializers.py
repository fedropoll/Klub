# services/serializers.py

from rest_framework import serializers
from .models import Service, Category
from branch.models import Branch  # <--- ЭТА СТРОКА ДОЛЖНА БЫТЬ ОБЯЗАТЕЛЬНО!
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    photo_url = serializers.SerializerMethodField()

    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), source='branch', write_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'price', 'duration_minutes',
            'photo', 'photo_url', 'is_active', 'branch_id',
            'category', 'category_name'
        ]
        read_only_fields = ['id', 'photo_url', 'category_name']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        elif obj.photo:
            return settings.MEDIA_URL + str(obj.photo)
        return None

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной.")
        return value

    def validate_duration_minutes(self, value):
        if value < 15:
            raise serializers.ValidationError("Минимальная длительность — 15 минут.")
        return value