
from django.core.mail import EmailMultiAlternatives
from django.dispatch import Signal, receiver
from django.conf import settings

from users.models import CustomUser

new_order_confirmation = Signal()

@receiver(new_order_confirmation)
def new_order_signal(user_id,**kwargs):

    # send an e-mail to the user
    user = CustomUser.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()