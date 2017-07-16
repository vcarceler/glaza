from django.conf import settings
from django.core.mail import send_mail

def notify(subject, body):
    '''Sends a email notification.'''

    send_mail(subject, body, settings.EMAIL_HOST_USER, settings.EMAIL_RECIPIENT_LIST, fail_silently=False)

