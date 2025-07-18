# list_doctor/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Branch # Импортируем Branch из этого же приложения

# Улучшенный DirectorField для гибкости
class DirectorField(serializers.RelatedField):
    queryset = User.objects.all()

    def to_representation(self, value):
        # Отображаем email директора
        return value.email

    def to_internal_value(self, data):
        # Принимаем либо ID пользователя, либо email
        if isinstance(data, int):
            try:
                return User.objects.get(id=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("Пользователь с таким ID не найден.")
        elif isinstance(data, str):
            try:
                return User.objects.get(email=data)
            except User.DoesNotExist:
                raise serializers.ValidationError("Пользователь с таким email не найден.")
        raise serializers.ValidationError("Ожидается ID или Email пользователя.")

class BranchSerializer(serializers.ModelSerializer):
    # Теперь director может быть передан как ID или email
    director = DirectorField(allow_null=True, required=False)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'director', 'phone_number']
        read_only_fields = ['id'] # ID только для чтения