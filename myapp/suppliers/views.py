# Create your views here.
import json
from django.db.models import Case, When, Value, F
from django.http import JsonResponse, HttpResponse
from requests import post
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Product, Category, Supplier

from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer


class CatalogView(ListAPIView):

    def get(self, request):
        category = request.GET.get("category")
        supplier = request.GET.get("supplier")
        if category:
            if supplier:
                goods = Product.objects.all().filter(category=category,supplier=supplier)
            else:
                goods = Product.objects.all().filter(category=category)
        else:
            if supplier:
                goods = Product.objects.all().filter(supplier=supplier)
            else:
                goods = Product.objects.all()
        ser = ProductSerializer(goods, many=True)
        return JsonResponse(ser.data, safe=False)


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierView(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierState(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')
        supplier = request.user.supplier
        serializer = SupplierSerializer(supplier)
        return JsonResponse(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')

        Supplier.objects.filter(user_id=request.user.id).update(state=Case(When(state=True, then=Value(False)),
                                                                           When(state=False, then=Value(True))))
        return HttpResponse('state changed')

class ProductImport(APIView):


    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')
        # В случае url ссылки
        # url = request.data.get('url')
        # if url:
        #     validate_url = URLValidator()
        #     try:
        #         validate_url(url)
        #     except ValidationError as e:
        #         return JsonResponse({'Status': False, 'Error': str(e)})
        #     else:
        #         stream = get(url).content
        #
        #         data = load_yaml(stream, Loader=Loader)


        with open("data/new_products.json", "r") as file:
            data = json.load(file)


        sup = Supplier.objects.get(user_id=request.user.id)

        for item in data['fields']:
            product, _ = Product.objects.get_or_create(name=item['name'],
                                                        category = Category.objects.get(id=item['category']),
                                                        description=item["description"],
                                                        price=item["price"],
                                                        quantity=item["quantity"])
            Product.objects.get(name=item['name']).supplier.set([sup.id])
        return HttpResponse('Upload successfully')


class PriceUpdate(APIView):

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse('Authorization needed')
        markup = request.data.get('markup')
        sup = Supplier.objects.get(user_id=request.user.id)
        prods = Product.objects.filter(supplier=sup.id)
        for i in prods:
            Product.objects.filter(supplier=sup.id).filter(id=i.id).update(price = F('price')*((100+markup)/100))
        return HttpResponse('Price updated')





