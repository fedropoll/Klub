from rest_framework import serializers
from .models import Branch
from main.models import CustomUser, UserProfile

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['email', 'first_name', 'last_name']

class BranchSerializer(serializers.ModelSerializer):
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(user_profile__role='director'),
        source='director',
        write_only=True
    )
    director_info = DirectorSerializer(source='director', read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'director_id', 'director_info', 'phone']
