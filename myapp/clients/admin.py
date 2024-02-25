from django.contrib import admin
from .models import  Order, OrderPosition


# Register your models here.

class OrderPositionInline(admin.TabularInline):
    model = OrderPosition
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [OrderPositionInline]


