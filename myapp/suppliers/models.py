from django.db import models
from users.models import CustomUser


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    user = models.OneToOneField(CustomUser, verbose_name='Пользователь',blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    state = models.BooleanField(verbose_name='Cтатус', default=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ManyToManyField(Supplier)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


    def __str__(self):
        return f'{self.name}'



