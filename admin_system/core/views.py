from rest_framework import viewsets, status
from rest_framework import generics
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, VersionHistory
from .permissions import IsAdminOrReadOnly
from .serializers import UserSerializer, GroupSerializer, PasswordChangeSerializer, CustomUserSerializer, \
    EmailChangeSerializer, UserProfileSerializer, VersionedModelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class PasswordChangeView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

class EmailChangeView(generics.UpdateAPIView):
    serializer_class = EmailChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    @action(detail=True, methods=['post'])
    def add_to_group(self, request, pk=None):
        user = self.get_object()
        group_name = request.data.get('group')
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return Response({'status': 'Utilisateur ajouté au groupe'})

    @action(detail=True, methods=['post'])
    def remove_from_group(self, request, pk=None):
        user = self.get_object()
        group_name = request.data.get('group')
        group = Group.objects.filter(name=group_name).first()
        if group:
            user.groups.remove(group)
            return Response({'status': 'Utilisateur retiré du groupe'})
        return Response({'status': 'Group non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        status = 'activé' if user.is_active else 'désactivé'
        return Response({'status': f"Utilisateur {status} avec succès"})

    def perform_create(self, serializer):
        serializer.save()
        user = serializer.instance

    def perform_update(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_profile(self, request, pk=None):
        user = self.get_object()
        profile_data = request.data.get('profile', {})
        serializer = UserProfileSerializer(user.userprofile, data=profile_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'Profile mis à jour avec succès'})

    @action(detail=True, methods=['get'])
    def get_versions(self, request, pk=None):
        user = self.get_object()
        # Suppose que l'historique est sauvegardé dans une table séparée pour `user`
        versions = user.history.all()  # Remplacez `history` par votre méthode d’historique
        serialized_versions = VersionedModelSerializer(versions, many=True)
        return Response(serialized_versions.data)

    @action(detail=True, methods=['post'])
    def restore_version(self, request, pk=None):
        user = self.get_object()
        version = request.data.get('version')
        if version:
            try:
                history_entry = VersionHistory.objects.get(content_type='CustomUser', object_id=user.id, version=version)
                for field, value in history_entry.data.items():
                    setattr(user, field, value)
                user.save()
                return Response({'status': f'Version {version} restaurée avec succès'})
            except VersionHistory.DoesNotExist:
                return Response({'error': "Version non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Version non spécifiée'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'is_active': self.user.is_active,
        })
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@action(detail=True, methods=['get'])
def get_versions(self, request, pk=None):
    instance = self.get_object()
    versions = instance.history.all()
    serialized_versions = VersionedModelSerializer(versions, mane=True)
    return Response(serialized_versions.data)