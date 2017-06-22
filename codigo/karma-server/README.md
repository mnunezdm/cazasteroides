# Karma Server

```
TODO
```

## Instalación

### Prerrequisitos

Sera necesario tener Python3 instalado. No se asegura el correcto funcionamiento sobre Python2. Para la instalar se puede realizar directamente desde la página web de [Python](https://www.python.org/downloads/)

Además, será necesario tener instalado pip para descargar todos los módulos necesarios, este paquete se instala por defecto al instalar cualquier versión de Python por encima de 2.7.8 y por encima de 3.3 (no inclusive).

Por último, es recomendable utilizar virtualenv para evitar que módulos no necesarios interfieran.

### Instalación

Habrá que descargarse la última versión del servidor desde este repositorio Git, para ello lo podemos hacer utilizando el siguiente mandato.

```
git clone https://github.com/mnunezdm/cazasteroides.git
```

Con esto activado habrá que navegar hasta la carpeta donde está el servidor, esta es:

```
cd cazasteroides/código/karma-server
```

Ahora, si se quiere utilizar un virtualenv habrá que inicializarlo y activarlo.

```
virtualenv .
Scripts/activate
```

Ahora, habrá que instalar todos los módulos necesarios, para ello, simplemente lanzaremos el mandato

```
pip install -r requirements.txt
```

Por último, tendremos que inicializar la base de datos.

Para ello, dentro de la carpeta src, lanzaremos los tres siguientes mandatos.

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Con esto ya tendremos nuestro sistema preparado para poder ejecutar el servidor.

## Probar Servidor

Se ha preparado una batería de test para probar todos los módulos de este servidor, para ello, tendremos que lanzar el siguiente mandato:

```
python manage.py runtests
```
