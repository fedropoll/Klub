from rest_framework import serializers
from .models import Branch
from django.contrib.auth.models import User

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class BranchSerializer(serializers.ModelSerializer):
    director = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    director_info = DirectorSerializer(source='director', read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'director', 'director_info', 'phone']
