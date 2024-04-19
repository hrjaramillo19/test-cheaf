from rest_framework import serializers
from apis.products.models import Product
from apis.notifications.serializers import AlertSerializer
from apis.notifications.models import Alert


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de Producto en donde se obtienen todos los campos.
    """

    class Meta:
        model = Product
        fields = "__all__"


class ProductAlertSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de Producto con Alerta en donde se obtienen todos los campos y tambien las alertas con las que cuenta dicho producto.
    """

    alerts = serializers.SerializerMethodField(method_name="get_alerts")

    def get_alerts(self, obj):
        alerts = Alert.objects.filter(product=obj)
        return AlertSerializer(alerts, many=True).data

    class Meta:
        model = Product
        fields = [
            "id",
            "deleted",
            "deleted_by_cascade",
            "name",
            "description",
            "stock",
            "date_of_expiry",
            "create_at",
            "alerts",
        ]
