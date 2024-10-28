from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, GroupViewSet, PasswordChangeView, EmailChangeView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('api/change-email/', EmailChangeView.as_view(), name='change-email'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
