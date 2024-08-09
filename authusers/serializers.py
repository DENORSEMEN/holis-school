from rest_framework import serializers
from .models import AuthUser
from rest_framework.validators import ValidationError
from django.utils import timezone


class SignUpSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    title = serializers.CharField(max_length=20, required=False, allow_blank=True)
    surname = serializers.CharField(max_length=50)
    firstname = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

    class Meta:
        model = AuthUser
        fields = ['email', 'title', 'surname', 'firstname', 'phone_number']


    def validate_username(self, value):
        """Ensure the username is unique."""
        if AuthUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken. Please choose a different one.")
        return value

    def validate(self, attrs):
        email_exists = AuthUser.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        # Create a user with default password 'student'
        user = AuthUser.objects.create_user(**validated_data, password='student')
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = AuthUser.objects.get(email=email, otp=otp)
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email")

        return data
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = AuthUser.objects.get(email=email)
            
            if user.otp != otp:
                raise serializers.ValidationError("Invalid OTP")
            
            if user.otp_expiry < timezone.now():
                raise serializers.ValidationError("OTP has expired")
            
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

        return data
    

from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['government_id_image', 'date_of_birth', 'gender', 'address']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['government_id_image', 'date_of_birth', 'gender', 'address']

class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['government_id_image', 'date_of_birth', 'gender', 'address']


from rest_framework import serializers
from .models import AuthUser, UserProfile

class UserProfileDetailSerializer(serializers.ModelSerializer):
    government_id = serializers.CharField(source='profile.government_id', allow_blank=True, required=False)
    date_of_birth = serializers.DateField(source='profile.date_of_birth', allow_null=True, required=False)
    gender = serializers.CharField(source='profile.gender', allow_blank=True, required=False)
    address = serializers.CharField(source='profile.address', allow_blank=True, required=False)

    class Meta:
        model = AuthUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'title', 'surname', 'phone_number', 'date_of_birth', 'government_id', 'gender', 'address']


from rest_framework import serializers

class ForgotUserIDSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Check if the email is associated with an account
        if not AuthUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value


from rest_framework import serializers
from .models import AccountRecoveryRequest

class AccountRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRecoveryRequest
        fields = ['email', 'government_id', 'photo']
