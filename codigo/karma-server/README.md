# Karma Server

```
TODO
```

## Instalación

### Prerequisitos

Sera necesario tener Python3 instalado. No se asegura el correcto funcionamiento sobre Python2. Para la instalar se puede realizar directamente desde la pagina web de [Python](https://www.python.org/downloads/)

Además, sera necesario tener instalado pip para descargar todos los modulos necesarios, este paquete se instala por defecto al instalar cualquier version de Python por encima de 2.7.8 y por encima de 3.3 (no inclusive).

Por ultimo es recomendable utiliar virtualenv para evitar que modulos no necesarios interfieran.

### Instalacion

Habra que descargarse la ultima version del servidor desde este repositorio Git, para ello lo podemos hacer utilizando el siguiente mandato.

```
git clone https://github.com/mnunezdm/cazasteroides.git
```

Con esto activado habra que navegar hasta la carpeta donde esta el servidor, esta es:

```
cd cazasteroides/codigo/karma-server
```

Ahora, si se quiere utilizar un virtualenv habra que inicilizarlo y activarlo.

```
virtualenv .
Scripts/activate
```

Ahora, habra que instalar todos los modulos necesarios, para ello, simplemente lanzaremos el mandato

```
pip install -r requirements.txt
```

Por ultimo, tendremos que inicializar la base de datos.

Para ello, dentro de la carpeta src, lanzaremos los tres siguientes mandatos.

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Con esto ya tendremos nuestro sistema preparado para poder ejecutar el servidor.

## Probar Servidor

```
TODO
```