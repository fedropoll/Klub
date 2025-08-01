from rest_framework import serializers

class SMSSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=20,
        help_text="Номер телефона в формате +996XXXXXXXXX"
    )
    message = serializers.CharField(
        max_length=255,
        help_text="Текст сообщения"
    )

    def validate_phone(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Номер должен начинаться с + и кода страны")
        if not value[1:].isdigit():
            raise serializers.ValidationError("Номер должен содержать только цифры после +")
        if len(value) < 10:
            raise serializers.ValidationError("Номер слишком короткий")
        return value
