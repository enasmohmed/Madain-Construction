from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from core.models import SiteSettings

from .models import ContactMessage


def get_contact_recipient():
    site = SiteSettings.objects.first()
    if site and site.email:
        return site.email
    return getattr(settings, "CONTACT_RECIPIENT_EMAIL", None) or settings.DEFAULT_FROM_EMAIL


def submit_contact_message(*, name, email, message, subject=None):
    subject = subject or _("Website message from %(name)s") % {"name": name}

    ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
    )

    recipient = get_contact_recipient()
    body = _(
        "Name: %(name)s\n"
        "Email: %(email)s\n\n"
        "%(message)s"
    ) % {"name": name, "email": email, "message": message}

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        reply_to=[email],
        fail_silently=False,
    )
