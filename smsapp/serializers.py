from rest_framework import serializers

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=15,
        required=True,
        help_text="Номер телефона в формате +996XXXXXXXXX"
    )

    def validate_phone(self, value):
        # Простейшая валидация формата номера
        if not value.startswith('+'):
            raise serializers.ValidationError('Номер должен начинаться с + и кода страны')
        if len(value) < 10:
            raise serializers.ValidationError('Номер слишком короткий')
        return value
