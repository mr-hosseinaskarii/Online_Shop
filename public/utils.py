from datetime import timedelta

from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from apps.accounts.models import Opt


def generate_code():
    opt_code = get_random_string(length=6, allowed_chars="0123456789")
    return opt_code


def send_otp_email(email, otp_code):
    subject = "Email Verification"
    message = f"""Hi, here is your OTP code:
    {otp_code}
    
    This code will expire in 2 minutes.
    """
    sender_email = settings.EMAIL_HOST_USER
    receiver_email = [email]

    send_mail(
        subject=subject,
        message=message,
        from_email=sender_email,
        recipient_list=receiver_email,
        fail_silently=False
    )


def generate_otp(user):
    code = generate_code()
    expiry = timezone.now() + timedelta(minutes=2)
    return Opt.objects.create(user=user, code=code, expired_at=expiry)
