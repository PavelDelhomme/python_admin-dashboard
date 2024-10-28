from django.contrib.auth.models import User, Group
from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import UserProfile, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Valider le nouveau mot de passe avec les validateurs de Django
        password_validation.validate_password(value, self.context['request'].user)
        return value

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get("old_password")):
            raise serializers.ValidationError({"old_password": "L'ancien mot de passe est incorrect."})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class EmailChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_email = serializers.EmailField(required=True)


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.email = self.validated_data['new_email']
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date', 'profile_picture']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    groups = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all(), many=True)
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone", "address", "is_active", "is_verified", "role", "groups", "profile"]

class VersionedModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["version", "last_modified", "created_at"]