import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification

def generate_verification_code():
    """Генерирует случайный код подтверждения (6 символов)."""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_code(email):
    """Генерирует код и отправляет его на указанный email."""
    # Генерация кода подтверждения
    code = generate_verification_code()

    # Сохраняем код в базе данных
    verification = EmailVerification.objects.create(
        email=email,
        code=code
    )

    # Отправляем email с кодом подтверждения
    subject = "Ваш код подтверждения"
    message = f"Ваш код подтверждения: {code}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

    return verification


