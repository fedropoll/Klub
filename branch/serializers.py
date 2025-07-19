from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Branch
from main.models import UserProfile

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class BranchSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(read_only=True)
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='director',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'phone_number', 'director', 'director_id')
        read_only_fields = ('director',)

    def validate_director_id(self, value):
        if value and not value.is_staff:
            raise serializers.ValidationError("Выбранный пользователь не является сотрудником и не может быть директором.")
        return value