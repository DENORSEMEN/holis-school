from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializers
    permission_classes = []  # Open to all

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()

            response = {
                "message": "User created successfully",
                "user_id": user.user_id,
                "email": user.email
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import authenticate

from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import AuthUser

class LoginView(APIView):
    permission_classes = []  # Open to all

    def post(self, request: Request):
        user_id = request.data.get('user_id')
        password = request.data.get('password', 'student')  # Default password

        user = authenticate(user_id=user_id, password=password)

        if user is not None:
            otp = generate_otp()
            user.set_otp(otp)  # Set OTP and its expiry time
            self.send_otp_email(user.email, otp)
            return Response(data={"message": "OTP sent to your email",
                                  "username": user.username,  # Assuming user object has a username field
                                  "email": user.email}, status=status.HTTP_200_OK)

        return Response(data={"message": "Invalid login"}, status=status.HTTP_401_UNAUTHORIZED)

    def send_otp_email(self, email, otp):
        """Send OTP to the user's email."""
        subject = 'Your OTP Code'
        message = f'Your OTP code is: {otp}'
        from_email = 'venvictor602@gmail.com'  # Replace with your actual sender email
        send_mail(subject, message, from_email, [email], fail_silently=False)

from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# @api_view(['POST'])
# @permission_classes([])
# def verify_otp_email(request):
#     serializer = VerifyOTPSerializer(data=request.data)
    
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         user = AuthUser.objects.get(email=email)
#         user.is_verified = True
#         user.otp = None  # Clear OTP after verification
#         user.save()
#         return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerifyOTPSerializer
from .models import AuthUser

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        try:
            user = AuthUser.objects.get(email=email)
            
            if user.otp != otp:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.otp_expiry < timezone.now():
                return Response({'message': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_verified = True
            user.otp = None  # Clear OTP after verification
            user.otp_expiry = None  # Clear OTP expiry time
            user.save()
            
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        
        except AuthUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create UserProfile for the currently authenticated user
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return user_profile

class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the UserProfile for the currently authenticated user
        user_profile = UserProfile.objects.get(user=self.request.user)
        return user_profile

class UserProfileCreateView(generics.CreateAPIView):
    serializer_class = UserProfileCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the profile with the currently authenticated user
        serializer.save(user=self.request.user)


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .models import AuthUser
from .serializers import UserProfileDetailSerializer

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user


class ForgotUserIDView(APIView):
    permission_classes = []  # Allow access to all users
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ForgotUserIDSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = AuthUser.objects.get(email=email)
                # Send an email with the user ID
                subject = 'Your User ID'
                message = f'Hello {user.first_name},\n\nYour User ID is: {user.user_id}'
                from_email = 'venvictor602@gmail.com'  # Replace with your email
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                
                return Response({"message": "User ID has been sent to your email."}, status=status.HTTP_200_OK)
            except AuthUser.DoesNotExist:
                return Response({"error": "No account found with this email."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)