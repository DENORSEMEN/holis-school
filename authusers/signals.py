from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import AuthUser

@receiver(post_save, sender=AuthUser)
def send_user_id_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Registration Successful'
        message = f'Your user ID is: {instance.user_id}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"Failed to send email: {e}")
