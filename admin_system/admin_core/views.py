from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import ProjectSetting
from rest_framework import viewsets
from .serializers import DynamicFieldsModelSerializer

class GenericModelViewSet(viewsets.ModelViewSet):
    serializer_class = DynamicFieldsModelSerializer

    def get_queryset(self):
        model = self.kwargs['model']
        return model.objects.all()

    def get_serializer_class(self):
        model = self.kwargs['model']
        return type(f"{model.__name__}Serializer", (DynamicFieldsModelSerializer,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})


class ProjectSettingView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = {setting.key: setting.value for setting in ProjectSetting.objects.all()}
        return Response(settings)

    def post(self, request):
        for key, value in request.data.items():
            setting, created = ProjectSetting.objects.get_or_create(key=key)
            setting.value = value
            setting.save()
        return Response({'status': 'Paramètres mis à jour avec succès'})