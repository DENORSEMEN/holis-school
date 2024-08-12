from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import random
import string
from django.core.mail import send_mail

def generate_unique_user_id(length=6):
    """Generate a unique user ID of a given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_otp(length=6):
    """Generate a random OTP of a given length."""
    return ''.join(random.choices(string.digits, k=length))


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user_id = generate_unique_user_id()  # Generate the unique user ID
        otp = generate_otp()

        extra_fields.setdefault('user_id', user_id)  # Set user_id in extra_fields
        extra_fields.setdefault('otp', otp)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password or "student")  # Default password is 'student'
        user.save(using=self._db)
        self.send_verification_email(email, otp)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)

    def send_verification_email(self, email, otp):
        """Send a verification email with the OTP."""
        subject = 'Verify your email'
        message = f'Your OTP for email verification is: {otp}'
        from_email = 'venvictor602@gmail.com'  # Replace with your actual sender email
        send_mail(subject, message, from_email, [email], fail_silently=False)

from django.utils import timezone
from datetime import timedelta
class AuthUser(AbstractUser):
    user_id = models.CharField(max_length=6, unique=True, default=generate_unique_user_id)
    email = models.EmailField(max_length=90, unique=True)
    username = models.CharField(max_length=56)  # Ensure username is unique
    title = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "user_id"  # Regular users login with user_id
    REQUIRED_FIELDS = ["username", "email", "surname", "firstname"]  # Superuser creation requires these fields

    def __str__(self):
        return f"{self.firstname} {self.surname}"
    
    def set_otp(self, otp):
        self.otp = otp
        self.otp_expiry = timezone.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    government_id_image = models.ImageField(upload_to='government_ids', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True)  # e.g., 'Male', 'Female', 'Other'
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
from django.db import models
from django.conf import settings
from django.core.mail import send_mail

class AccountRecoveryRequest(models.Model):
    email = models.EmailField()
    government_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='recovery_photos')
    submitted_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Recovery request for {self.email}"

    def save(self, *args, **kwargs):
        # Check if approved status changes from False to True
        if self.pk and not self.approved and self.approved:
            self.send_approval_email()

        super().save(*args, **kwargs)

    def send_approval_email(self):
        subject = 'Account Recovery Approved'
        message = 'Your account recovery request has been approved. You can now reset your password.'
        from_email = 'venvictor602@gmail.com.com'  # Replace with your email
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
