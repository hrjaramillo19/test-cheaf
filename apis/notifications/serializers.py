from rest_framework import serializers
from apis.notifications.models import Alert


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de Alerta en donde se obtienen todos los campos.
    """

    class Meta:
        model = Alert
        fields = "__all__"
