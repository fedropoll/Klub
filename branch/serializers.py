from rest_framework import serializers
from .models import Branch
from main.models import CustomUser, UserProfile

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['email', 'first_name', 'last_name']

class BranchSerializer(serializers.ModelSerializer):
    director_info = DirectorSerializer(source='director', read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'director_info', 'phone']

    def create(self, validated_data):
        director = CustomUser.objects.filter(user_profile__role='director').first()
        if not director:
            raise serializers.ValidationError("Директор не найден.")
        validated_data['director'] = director
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('director', None)
        return super().update(instance, validated_data)
