# Analisis y Propuesta de Mejora

## Aplicacion

Se ha realizado un rediseño de la aplicacion móvil siguiendo las guias de Material Design, una de las guias de diseño mas importantes que hay en la actualidad, desarrollada por Google. Este rediseño se debe a dos razones, la navegación aun siendo intuitiva no es la que mejor para este caso y por otro lado, la apariencia de la aplicacion no es de una aplicacion terminada.

### Navegacion

Para lograr esta mejor navegacion se ha decidido aumentar el numero de pantallas que tiene la aplicacion. Para ilustrar estos cambios en la Figura 1 tenemos una comparacion de los esquemas de la navegacion, donde las burbujas serian cada una de estas pantallas. A continuacion se van a explicar la funcion actual y la nueva que tienen estas pantallas. En el esquema planteado, las burbujas azules tendrian la misma funcionalidad en las dos aplicaciones y las verdes se habria modificado esta funcionalidad.

![Figura 1: Comparacion Esquemas de Navegación](imgs/comparacionEsquemas.png)

1. **Login**: esta pantalla va a ser la primera pantalla que cargara la aplicación. Permitira a los usuarios hacer login con una cuenta ya creada, registrarse o pedir un reseteo de contraseña.
2. **Registro**: permite al usuario registrarse, ya sea por medio de correo y contraseña o utilizando el login por token con google o facebook.
3. **Splash Screen**: esta va a ser una pantalla de carga, cuando ya nos hayamos logeado en la aplicacion esta pasara a ser la primera pantalla que abrira la aplicación. Realizara la carga de todos los datos que necesite cargar para su correcto funcionamiento.
4. **Pantalla Principal**: esta va a ser la pantalla principal de nuestra aplicacion, seria la primera pantalla en la pila, es decir, pulsando atras deberiamos salir de la aplicacion. Esta pantalla se ha pensado como una barra de navegacion inferior de Material Design con los botones a las acciones principales que va a tener nuestra aplicacion. Estas acciones cambiarian el panel mostrado en la pantalla. Los botones serían los siguientes:
	1. **Home**: se trata del panel por defecto, este panel se ha pensado como un resumen de toda la actividad del usuario. Contiene información del usuario asi como un acceso a la edicion de esta informacion, estadisticas y el acerca de.
	2. **Interacciones**: en este panel apareceran todas las observaciones y las visualizaciones realizadas por el usuario (informacion separada en dos pestañas). Esto permite al usuario ver si sus interacciones con el sistema han sido correctas o no.
	3. **Votaciones**: en este panel aparecera un listado de unas pocas observaciones realizadas por otros usuarios permitiendo al usuario ver la imagen y votar si creen o no que se trate de un asteroide.
	4. **Ranking**: este panel tendra distintas pestañas con el top 10 de usuarios de distintos rankings, ademas de la posicion actual del usuario.
5. **Editar Perfil**: en esta pantalla el usuario podra editar su perfil.
6. **Estadisticas**: en esta pantalla se mostraran distintas estadisticas sobre el uso de la aplicacion, tanto globales como del propio usuario.
7. **Acerca De**: en esta pantalla se mostrara informacion de la aplicacion, principalmente servira para mostrar cual es el proposito de la aplicacion (ya que muchos usuarios la usan sin saberlo), informacion sobre los integrantes y mas datos (ir)relevantes.
8. **Carga Observacion**: esta pantalla sera una pantalla de carga la cual no se superara hasta que no se hayan descargado todas las imagenes, es necesaria esta pantalla pues en conexiones lentas se han llegado a tener 20 segundos de carga lo cual repercutia directamente en la puntuacion obtenida. Tras esta pantalla aparecera la pantalla Nueva Observacion.
8. **Nueva Observacion**: esta pantalla sera muy similar a la de la version anterior, salvo que la comunicacion con el sistema se hara al confirmar una observacion y no con cada toque lo cual suponia demasiadas peticiones al sistema que influian en el rendimiento de la aplicacion.
9. **Observacion Detallada**: esta pantalla tendra informacion sobre la observacion, la pantalla sera la misma ya sea una observacion propia o una observacion de otra persona. Tendra informacion simple, compleja y datos del ranking, como podria ser tiempo, puntuacion o dificultad. Ademas mostraria en el estado en el que se encuentra esta observacion.

### Apariencia



## Sistema de Gamificación y Reputación

Utilizando los conocimientos adquiridos al analizar las distintas tecnicas de gamificacion y reputacion vistas en el anterior capitulo (Estado del Arte) se ha decidido ampliar el actual sistema con el fin de lograr unos resultados más acordes. Los distintos apartados a desarrollar, asi como las mejoras planteadas se van a especificar a continuacion:

### Plataforma

En estos momentos las plataformas donde esta integrado el sistema son solamente el propio servidor Node.js y el sistema operativo Android donde hay una aplicación funcional.

Como propuesta de mejora para este apartado se propone que la aplicacion este disponible en los dos grandes sistemas operativos móviles. Ademas de lograr una mayor integracion con las Redes Sociales, convirtiendolas en fundamentales para el sistema.

### Mecanicas

Actualmente las mecanicas de juego implementadas en el sistema son las 
Las mecanicas de juego que se tiene pensado utilar son las siguientes.

+ **Puntuación**: actualmente ya se encuentra implantado aunque se le va a dar mayor complejidad.
+ **Karma**: un sistema de reputacion que aumentaria del mismo modo que la puntuacion. Nunca se reduce este nivel. Otorga mayor importancia al usuario, haciendo que sus acciones tengo mayor relevancia que la del resto de usuarios.
+ **Insignias**: distintas medallas que obtendrian los usuarios de distintas maneras.
+ **Retos**: misiones que los usuarios pueden lanzar a otros.
+ **Premios** reales: en el caso de cazasteroides, se va a permitir utilizar los puntos obtenidos para canjearlos por tiempo de operacion de la red de telescopios Gloria.
+ **Clasificaciones**: al igual que el sistema de puntuacion, ya se encuentra implementando y se va a rediseñar para incrementar la informacion que aportan.

### Dinamicas

Las dinamicas pensadas para casteroides son las siguientes:

+ **Realizar observaciones**: uno de los objetivos principales de la aplicacion. Realizando observaciones (es decir buscando asteroides en imagenes). Se obtienen puntos y karma segun distintos parametros.
+ **Realizar votaciones**: el otro objetivo princiapal del juego. Permitir votar a los usuarios las observaciones realizadas por otros usuarios.
+ **Completar misiones diarias**: simples misiones que den puntos por completar algunas tareas, ayudan a que el usuario sienta la necesidad de entrar diariamente.
+ **Completar logros**: misiones mas complejas y largas que obliguen al usuario a jugar mucho y a usar todas las caracteristicas. Estos logros otorgaran insignias al usuario. Muy importante conectar esto con plataformas como Google Play Games, para que estos logros aumenten tambien el perfil del usuario no solo en el juego lo que aumenta las ganas de jugar.
+ **Visualizar Rankings**: permitir al usuario ver como se encuentra el con respecto al mundo.
+ **Compartir observaciones**: permite al usuario compartir por redes sociales una observacion que ha realizado.
+ **Lanzar retos**: permite al usuario lanzar retos por redes sociales para competir de forma directa con sus amigos.
+ **Comprar tiempo en el observatorio**: permitir a los usuarios gastar los puntos acumulados en algo real, dando sentido al tiempo invertido en el juego.

### Esteticas

En nuestro caso las distintas esteticas presentes son:

+ **Desafiante**: queremos que el usuario se esfuerce en superarse a si mismo y a los demas.
+ **Descubrimiento**: queremos que el usuario aprenda y explore un mundo que nunca haya visto.
+ **Expresivo**: queremos que el usuario se comunique con otros usuarios.

## Referencias

+ Justinmind por la aplicacion de prototipado
+ Google por las guias de diseño de Material Design
+ Google por Material Design Icons 
+ FlatIcon 
	+ Ranking: Freepik
	+ Telecope: Freepik
	+ Meteor: Nikita Golubev
