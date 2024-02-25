from django.db import models

from suppliers.models import Product

from users.models import CustomUser


# Create your models here.
STATE_CHOICES = (
    ('new', 'Новый'),
    ('in_process', 'В_процессе'),
    ('completed', 'Завершен'),
)
class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders', through='OrderPosition')
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', blank=True, null=True,
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(null=True, blank=True)
    state = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15, default="new")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"



class OrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='positions')
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Заказанные позиции"