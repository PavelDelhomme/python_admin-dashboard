from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenericModelViewSet, ProjectSettingView

router = DefaultRouter()
router.register(r'<str:model>/', GenericModelViewSet, basename='model')

urlpatterns = [
    path('api/admin/', include(router.urls)),
    path('settings/', ProjectSettingView.as_view(), name='project-settings'),
]
