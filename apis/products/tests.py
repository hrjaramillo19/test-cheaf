from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apis.products.models import Product
from datetime import datetime


class ProductsAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test_user", email="test_user@email.com", password="test_password"
        )
        cls.client = APIClient()

    def authenticate_user(self):
        data = {"username": "test_user", "password": "test_password"}
        response = self.client.post("/api/v1/token/", data)
        return response.data.get("access")

    """
    Test unitario de creacion de producto
    """

    def test_01_product_create(self):
        # teste para crear un producto
        token = self.authenticate_user()
        data = {
            "name": "caramelo2",
            "stock": 50,
            "description": "caramelo2 en funda",
            "date_of_expiry": "2024-04-25",
        }
        response = self.client.post(
            "/api/v1/products/create_product/",
            data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name, "caramelo2")
        self.assertEqual(product.stock, 50)
        self.assertEqual(product.description, "caramelo2 en funda")
        self.assertEqual(product.date_of_expiry.strftime("%Y-%m-%d"), "2024-04-25")

    def test_02_prodcut_create_missing_fields(self):
        # test para crear un producto si falta el campo name que es obligatorio
        token = self.authenticate_user()
        data = {"description": "caramelo2 en funda", "date_of_expiry": "2024-04-25"}
        response = self.client.post(
            "/api/v1/products/create_product/",
            data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_03_product_create_date_invalid(self):
        # test para crear un producto con una fecha invalida
        token = self.authenticate_user()
        data = {
            "name": "caramelo2",
            "stock": 50,
            "description": "caramelo2 en funda",
            "date_of_expiry": "2022/01/01",
        }
        response = self.client.post(
            "/api/v1/products/create_product/",
            data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test unitario para obtener un producto
    """

    def test_04_get_detail_product_exists(self):
        # test para obtener un producto que existe
        token = self.authenticate_user()
        data = {
            "name": "caramelo2",
            "stock": 50,
            "description": "caramelo2 en funda",
            "date_of_expiry": datetime.strptime("2024-04-25", "%Y-%m-%d"),
        }
        product = Product.objects.create(**data)
        url = f"/api/v1/products/{product.pk}/get_detail/"
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], product.name)
        self.assertEqual(response.data["stock"], product.stock)
        self.assertEqual(response.data["description"], product.description)

    def test_05_get_detail_product_not_exist(self):
        # test para obtener un producto que no existe
        token = self.authenticate_user()
        url = "/api/v1/products/99/get_detail/"
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Test unitario para obtener el listado de  productos
    """

    def test_06_get_all_products_with_valid_dates(self):
        # test para obtener todos los productos en rango de fechas válidas
        token = self.authenticate_user()
        url = "/api/v1/products/get_all/"
        start_date = "2024-04-01"
        end_date = "2024-04-25"
        response = self.client.get(
            url,
            {"start_date": start_date, "end_date": end_date},
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_07_get_all_products_with_invalid_dates(self):
        # Test para obtener todos los productos en rango fechas inválidas
        token = self.authenticate_user()
        url = "/api/v1/products/get_all/"
        start_date = "2024/04/30"
        end_date = "2024/04/25"
        response = self.client.get(
            url,
            {"start_date": start_date, "end_date": end_date},
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test unitario para actualizar un producto
    """

    def test_08_update_product_with_valid_data(self):
        # Test para Actualizar el producto con datos válidos
        token = self.authenticate_user()
        data = {
            "name": "caramelo2",
            "stock": 50,
            "description": "caramelo2 en funda",
            "date_of_expiry": datetime.strptime("2024-04-25", "%Y-%m-%d"),
        }
        product = Product.objects.create(**data)
        url = f"/api/v1/products/{product.id}/update_product/"
        data = {
            "name": "Yogurt",
            "stock": 10,
            "description": "Yogurt en funda",
            "date_of_expiry": "2024-05-10",
        }
        response = self.client.put(
            url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.name, data["name"])
        self.assertEqual(updated_product.stock, data["stock"])
        self.assertEqual(updated_product.description, data["description"])
        self.assertEqual(str(updated_product.date_of_expiry), data["date_of_expiry"])

    def test_09_update_product_with_invalid_data(self):
        # Test para actualizar el producto con datos inválidos
        token = self.authenticate_user()
        data = {
            "name": "caramelo2",
            "stock": 50,
            "description": "caramelo2 en funda",
            "date_of_expiry": datetime.strptime("2024-04-25", "%Y-%m-%d"),
        }
        product = Product.objects.create(**data)

        url = f"/api/v1/products/{product.id}/update_product/"
        data = {
            # Aquí falta el campo "name" que es requerido
            "stock": 10,
            "description": "Yogurt en funda",
            "date_of_expiry": "2024-05-10",
        }
        response = self.client.put(
            url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_10_update_nonexistent_product(self):
        # Test para actualizar un producto que no existe
        token = self.authenticate_user()
        url = "/api/v1/products/99/update_product/"
        data = {
            "name": "Yogurt",
            "stock": 10,
            "description": "Yogurt en funda",
            "date_of_expiry": "2024-05-10",
        }
        response = self.client.put(
            url,
            data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Test unitario para eliminar  un producto
    """

    def test_11_delete_product(self):
        # test para Eliminar un producto existente
        token = self.authenticate_user()
        data = {
            "name": "caramelo2",
            "stock": 50,
            "description": "caramelo2 en funda",
            "date_of_expiry": datetime.strptime("2024-04-25", "%Y-%m-%d"),
        }
        product = Product.objects.create(**data)

        url = f"/api/v1/products/{product.id}/delete_product/"
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_product(self):
        # test para eliminar un producto que no existe
        token = self.authenticate_user()
        url = "/api/v1/products/99/delete_product/"
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 404)
