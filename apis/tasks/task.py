from celery import shared_task
from django.core.mail import send_mail

"""
Archivo donde se colocan las task a ejecutar en celery
"""


@shared_task
def send_notification():
    send_mail(
        "Asunto del correo",
        "Cuerpo del correo.",
        "remitente@example.com",
        ["destinatario@example.com"],
        fail_silently=False,
    )
