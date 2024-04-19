from django.db import models
from safedelete.models import SafeDeleteModel


class Product(SafeDeleteModel):
    """
    Modelo para representar un producto en el inventario.

    Campos:
    - name: El nombre del producto.
    - description: Descripción del producto.
    - stock: cantidad disponible del producto.
    - date_of_expiry: fecha de expiracion.
    - create_at: fecha en la que se realizo el registro

    Se utiliza SafeDeleteModel para tener un eliminado logico de los prodcutos en la base de datos
    """

    name = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=1000, blank=True)
    stock = models.IntegerField(default=0)
    date_of_expiry = models.DateField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("name",)

    def __str__(self):
        return self.name
