from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from orders.models import RepairRequest


@receiver(post_save, sender=RepairRequest)
def send_notification_email(sender, instance, created, **kwargs):
    if not created and instance.status == "Готово к выдаче":
        subject = f"Ваша заявка на ремонт: {instance}"
        review_url = reverse("orders:add_review", kwargs={"token": instance.token})
        absolute_review_url = f"{settings.SITE_URL}{review_url}"
        message = render_to_string(
            "orders/email/notification.txt",
            {"instance": instance, "review_url": absolute_review_url},
        )
        recipient_list = [instance.email] if instance.email else None
        if recipient_list is not None:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
