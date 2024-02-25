from django.db import IntegrityError
from django.db.models import Sum, F, Count
from django.http import JsonResponse, HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .models import Order, OrderPosition
from .serializers import OrderSerializer, OrderPositionSerializer
from .signals import new_order_confirmation


# Create your views here.

class OrderView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderPositionView(ListAPIView):
    queryset = OrderPosition.objects.all()
    serializer_class = OrderPositionSerializer


class SupplierOrders(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')
        supplier = request.user.supplier
        orders = OrderPosition.objects.all().filter(product__supplier=supplier)
        serializer = OrderPositionSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)


class CartView(APIView):

    def get(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')
        cart = Order.objects.all().filter(user_id=request.user.id, state='new')
        serializer = OrderSerializer(cart, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')

        goods = request.data.get('goods')
        cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='new')
        objects_created = 0
        for good_item in goods:
            good_item.update({'order': cart.id})
            serializer = OrderPositionSerializer(data=good_item)
            if serializer.is_valid():
                try:
                    serializer.save()
                except IntegrityError as error:
                    return JsonResponse({'Status': False, 'Errors': str(error)})
                else:
                    objects_created += 1
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': True, 'Создано объектов': objects_created})

    def delete(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')

        goods = request.data.get('goods')
        if goods:
            items_list = goods.split(',')
            cart, _ = Order.objects.get_or_create(user_id=request.user.id)
            objects_deleted = 0
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    OrderPosition.objects.filter(order_id=cart.id, product_id=order_item_id).delete()[0]
                    objects_deleted += 1
            return JsonResponse({'Status': True, 'Удалено объектов': objects_deleted})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ClientView(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')

        order = Order.objects.filter(user_id=request.user.id).exclude(state='new')

        serializer = OrderSerializer(order, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')

        new_order = Order.objects.filter(user_id=request.user.id, state='new').update(state='in_progress')
        return HttpResponse('Order in progress')
        if new_order:
            new_order_confirmation.send(sender=self.__class__, user_id=request.user.id)
            return JsonResponse({'Status': True})
