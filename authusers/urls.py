from .views import *
from django.urls import path
from rest_framework_simplejwt.views import *
from django.conf.urls.static import static
urlpatterns = [
    path("register/", SignUpView.as_view(), name = "signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name = 'token_verify'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/', UserProfileDetailView.as_view(), name='profile'),
    path('create-profile/', UserProfileCreateView.as_view(), name='create-profile'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('forgot-user-id/', ForgotUserIDView.as_view(), name='forgot-user-id'),
#after adding the jwt make migrations
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
