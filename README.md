# Prueba Técnica: Desarrollo de API con Django para Gestión de Stock y Alertas de Caducidad

El desarrollo de la prueba tecnica se desarrollo con Django Rest Framework y para su despliege se utilizo docker

## Requerimientos de software
* Docker
* Docker compose


## Que se encuentra desplegado en el contenedor docker

1. api

Aca encontraremos el proyecto en Django Rest Framework

2. postgres

Aca tenemos levantada la base de datos del proyecto

3. nginx

Aca utilizamos el nginx para el enrutamiento y redireccion

4. mailhog

Se utilizo para la simulacion de envio de correos cuando esta proximo a caducar un producto

5. celery

Se utilizo para la recepcion y ejecucion de tareas asincronas, en este caso para el envio de los correos

6. redis

Se utiliza para almacer los datos en memoria necesarios para celery

7. flower

Es donde se encuentra la interfaz de administracion de Celery

## Pasos para depliegue del proyecto

Las configuraciones generales se encuentra en archivos para las variables de entorno en el archivo **.env.django** se encuentran las variables de entorno necesarias para las configuraciones de django y en el archivo **.env.postgres** se encuentras las configuraciones para la base de datos

El proyecto se debe levantar utilizando los comandos de **docker compose** ya que se ha realizado la configuracion del archivo .yaml

al ejecutar el siguiente comando se procedera con la construir el proyecto y el despliegue automatico

```docker compose -f local.yml up --build -d --remove-orphans```

una vez se encuentre levantado el proyecto procedemos con las migraciones para lo cual primero se ejecutara el makemigrations y posterior el migrate comando de django 

```docker compose -f local.yml run --rm api python3 manage.py makemigrations```

```docker compose -f local.yml run --rm api python3 manage.py migrate```

luego podremos crear nuestro usuario

```docker compose -f local.yml run --rm api python3 manage.py createsuperuser```

si se requiere ver los logs se debe ejecutar el siguiente comando

```docker compose -f local.yml logs -f api```

para detener o levantar el el proyecto se utilizan los siguientes comandos respectivamente

```docker compose -f local.yml down```

```	docker compose -f local.yml up -d```

## Uso de endpoints realizados


### obtener token de autenticaion

```
method: POST
url: http://localhost:8080/api/v1/token/
body-raw:
{
    "username": "admin",
    "password": "1234"
}
```

para todos los endpoint de ahora en adelante se debe utilizar el token de acceso de la respuesta obtenida
```
header 'Content-Type: application/json'

header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzNDI3Nzc1LCJqdGkiOiI4YzUyYjkwYjZhZWM0ODI4ODI3MzI5YzIwNDFmZGRhZiIsInVzZXJfaWQiOjF9.42hNzQTp852Yik2LRyMtVNlYeIdxZtNVrGmKRfTJUnM' 

```

### Crear producto

```
method: POST
url: http://localhost:8080/api/v1/products/create_product/
body-raw:
{
    "name": "caramelo2",
    "stock": 50,
    "description": "caramelo2 en funda",
    "date_of_expiry": "2024-04-25"
}
```


### Obtener el detalle de un producto

```
method: GET
url: http://localhost:8080/api/v1/products/<id_producto>/get_detail

```

### Obtener todos los productos

aca podemos enviar los paramtros de manera opcional **start_date** y **end_date** para obtener los productos deacuerdo al rango de fecha proximos a caducarse en formato de envio de las fechas debe ser ***yyyy-mm-dd***, y **alert_status** para obtener los productos deacuerdo al estado de la alerta sus valores pueden ser activate o expired

```
method: GET
url: http://localhost:8080/api/v1/products/get_all/?start_date=2024-04-01&end_date=2024-04-25&alert_status=active

```

### Actualizar un producto

```
method: PUT
url: http://localhost:8080/api/v1/products/<id_producto>/update_product/
body-raw:
{
    "name": "Yogurt",
    "stock": 10,
    "description": "Yogurt en funda",
    "date_of_expiry": "2024-05-10"
}
```

### Eliminar un producto

```
method: DELETE
url: http://localhost:8080/api/v1/products/<id_producto>/delete_product/
```

cabe indicar que se cuenta con un crontab para revisar las alertas proximas a caducar y actualizar el numero de dias restantes, y si ya es momento de enviar la alerta la enviaria mediante celery


## Ejecucion de test

Para la ejecución de los test se debe ejecutar el siguiente comando

```
docker compose -f local.yml run --rm api python3 manage.py test

```