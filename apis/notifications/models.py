from django.db import models
from safedelete.models import SafeDeleteModel
from enumchoicefield import EnumChoiceField
from apis.notifications.enum import StatusEnum
from datetime import datetime
from apis.products.models import Product
from django.db import models
from apis.products.utils import get_missing_days
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class Alert(SafeDeleteModel):
    """
    Modelo para representar una alerta.

    Campos:
    - product: es la relacion del producto con la alerta.
    - message: guardamos un mensaje para la alerta.
    - status: es el estado en el que se encuentra la alerta puede ser active o expire.
    - number_days_activate: numero de dias para la activacion de la alerta.
    - number_days_have_passed: numero de dias que han pasado despues de activar la alerta
    - date_activate: fecha de activacion de la alierta

    Se utiliza SafeDeleteModel para tener un eliminado logico de las alertas en la base de datos
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="alert_product"
    )
    message = models.CharField(max_length=255)
    status = EnumChoiceField(StatusEnum, default=StatusEnum.active)
    number_days_activate = models.IntegerField(default=0)
    number_days_have_passed = models.IntegerField(default=0)
    date_activate = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        ordering = ("date_activate",)

    def __str__(self):
        return f"{self.product.name} - {self.date_activate}"


def generate_alerts_product(product):
    limit_10_days = product.date_of_expiry - timedelta(days=10)
    limit_5_days = product.date_of_expiry - timedelta(days=5)
    missing_days_10 = get_missing_days(limit_10_days)
    dict_save_10 = {
        "product": product,
        "message": f"Faltan 10 días para la caducidad de {product.name}",
        "number_days_activate": missing_days_10,
        "date_activate": limit_10_days,
        "status": StatusEnum.expire if missing_days_10 > 0 else StatusEnum.active,
    }
    Alert.objects.create(**dict_save_10)
    missing_days_5 = get_missing_days(limit_5_days)

    dict_save_5 = {
        "product": product,
        "message": f"Faltan 5 días para la caducidad de {product.name}",
        "number_days_activate": missing_days_5,
        "date_activate": limit_5_days,
        "status": StatusEnum.expire if missing_days_5 > 0 else StatusEnum.active,
    }
    Alert.objects.create(**dict_save_5)


@receiver(post_save, sender=Product)
def generate_alerts_new_product(sender, instance, created, **kwargs):
    if created:
        generate_alerts_product(instance)
