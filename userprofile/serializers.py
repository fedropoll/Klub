# userprofile/serializers.py

from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'birth_date', 'gender', 'phone',
            'email', 'experience', 'address', 'status', 'about'
        ]
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile']
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)

        if profile_data:
            profile_serializer = self.fields['profile']
            profile_instance = instance.profile
            profile_serializer.update(profile_instance, profile_data)

        return user