
from django.core.mail import EmailMultiAlternatives
from django.dispatch import Signal, receiver
from django.conf import settings
from users.models import CustomUser
from .tasks import send_email_task

new_order_confirmation = Signal()

# Celery task
@receiver(new_order_confirmation)
def new_order_signal(user_id, **kwargs):
    user = CustomUser.objects.get(id=user_id)
    subject = "Order Status Update"
    message = "Your order has been placed."
    recipient = user.email
    send_email_task.delay(subject, message, recipient)


# @receiver(new_order_confirmation)
# def new_order_signal(user_id,**kwargs):
#
#     # send an e-mail to the user
#     user = CustomUser.objects.get(id=user_id)
#
#     msg = EmailMultiAlternatives(
#         # title:
#         f"Обновление статуса заказа",
#         # message:
#         'Заказ сформирован',
#         # from:
#         settings.EMAIL_HOST_USER,
#         # to:
#         [user.email]
#     )
#     msg.send()