from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from apis.products.models import Product
from apis.products.serializers import ProductSerializer, ProductAlertSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from apis.notifications.enum import StatusEnum


class ProductViewSet(viewsets.ModelViewSet):
    """
    Vista para manejar operaciones CRUD en el modelo de Producto.

    Permisos:
    - Se requiere autenticación para todas las operaciones.

    Métodos HTTP admitidos:
    - GET: Obtener lista de productos y detalles de un producto.
    - POST: Crear un nuevo producto.
    - PUT: Actualizar un producto existente.
    - DELETE: Eliminar un producto.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def get_all(self, request):
        dict_search = {}
        if "alert_status" in request.query_params:
            dict_search["alert_product__status"] = StatusEnum.active
        if "start_date" in request.query_params and "end_date" in request.query_params:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                dict_search["date_of_expiry__range"] = [start_date, end_date]
                products = Product.objects.filter(**dict_search)
                product_serializer = ProductAlertSerializer(products, many=True)
                return Response(product_serializer.data)
            except Exception as e:
                return Response([], status=400)
        else:
            queryset = Product.objects.filter(**dict_search)
            serializer = ProductAlertSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_detail(self, request, pk=None):
        producto = self.get_object()
        serializer = self.get_serializer(producto)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def create_product(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["put"])
    def update_product(self, request, pk=None):
        producto = self.get_object()
        serializer = self.get_serializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["delete"])
    def delete_product(self, request, pk=None):
        producto = self.get_object()
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
