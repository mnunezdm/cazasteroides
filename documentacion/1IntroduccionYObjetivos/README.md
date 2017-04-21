# Introduccion y objetivos

Cazasteroides se trata de un proyecto de ciencia ciudadana desarrollado en conjunto entre la Universidad Politécnica de Madrid y el Instituto Astrofísico de Canarias. 

El objetivo de este proyecto es realizar un experimento con el que acercar la astronomia a la ciudadania. Esto se va a conseguir convirtiendo a los usuarios de la aplicacion en *cazadores de asteroides*. Para ello los usuarios deberan localizar asteroides cercanos a la Tierra utilizando imagenes obtenidas por la red de telescopios GLORIA. Todas las observaciones probables seran enviadas al *Minor Planet Center* de la Union Internacional de Astronomia (IAU, International Astronomy Union).

Para lograr una mayor aceptacion por los usuarios se ha decidido utilizar tecnicas de gamificacion para acercar el concepto de *Games With A Purpose*. Gamificar consiste en acercar el concepto de juego a una idea. En este caso sería atribuir puntos a hallazgos y votaciones y así aumentar el karma, proponer retos, recompensar a los mejores jugadores...

Actualmente, el sistema se encuentra en fase beta donde aun con algun que otro *bug* la aplicacion es perfectamente utilizable. Este sistema se trata de una arquitectura REST. El esquema del sistema actual es el siguiente:

+ **Cliente**: programado en HTML5, CSS y JavaScript, concretamente utilizando el framework AngularJS. Partiendo de este código, utilizando la herramienta Apache Cordova se construyen aplicaciones nativas para Android e iOS. Ahora mismo solo hay dos versiones accesibles, estas son:
    + **Aplicacion Android**: la cual puede ser descargada desde la *Play Store* 
    + **Aplicacion Web *Responsive***: a la cual se puede acceder desde la pagina web de cazasteroides.
+ **Servidor**: tendríamos un servidor programado en Node.js.
+ **Base de datos**: concretamente MongoDB, tipo de base de datos que se caracteriza por tener un esquema dinámico de datos, aunque utilizaremos Mongoose, un plug-in de Node.js, que a parte de realizar las consultas, permite modelar los datos.
+ **Procesador de imágenes**: es el encargado de realizar todo el procesamiento de las imágenes de los telescopios, como es el recorte de la imagen original, la escala, y la compresión. Además, genera la animación de la observación.

El código del proyecto se encuentra alojado en BitBucket, una implementación de Git en la nube. Con esto conseguimos un control de versiones que tiene interesantes funcionalidades para el trabajo en grupo, como pueden ser:

+ **Control de versiones**: permite tener controlados todos los cambios, si fuese necesario se podría ver un estado del proyecto pasado, o volver a el.
+ **Issues**: permite crear incidencias con errores encontrados o funcionalidades que sean necesarias añadir.
+ **Branches**: permite trabajar en paralelo sobre dos funcionalidades distintas sin que un desarrollo afecte a otro.
 
Toda la documentación va a estar alojada en una carpeta compartida en la nube que permitirá a los supervisores del proyecto llevar un control regular del trabajo, además de que permite realizar comentarios y ofrece un sencillo control de versiones.

La metodología planteada para la realizacion de este proyecto es un desarrollo ágil. Como ahora mismo no se sigue una metodología de este tipo se va a llevar a cabo una transición. Destacando las siguientes métodos a seguir:

+ **Reuniones semanales** en las que analizar el avance realizado.
+ **Ramas**: se trabajará en distintas ramas lo que permitirá trabajar en distintos elementos sin que unos alteren al resto.
+ **Sprints**: Se marcarán objetivos a corto plazo de los requisitos más importantes intentando solo trabajar en una funcionalidad a la vez. Esto lo realizaremos mediante features (bifurcaciones de la rama principal). Cuando se termine una funcionalidad esta se unirá a la rama de desarrollo y se cerrará (si fuera necesario).