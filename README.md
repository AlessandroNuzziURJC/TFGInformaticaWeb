# P-3CO: Plataforma de Programación Paralela en Clúster con OpenStack

## Descripción
P-3CO (Plataforma de Programación Paralela en Clúster con OpenStack) es una aplicación web que permite la ejecución de programas escritos en C en el clúster Clea. Su función principal es presentar y analizar los tiempos y costes de la ejecución de algoritmos en distintos tipos de instancias. Esta aplicación responde a la necesidad común de desarrolladores e investigadores de ejecutar experimentos en un clúster y obtener un cálculo del tiempo y el coste involucrados. Gracias a la aplicación se obtiene una estimación del coste que conlleva poner un software paralelo en producción y permitir comparar dicho coste con la versión secuencial del mismo.

La aplicación está montada sobre Clea, utilizando la infraestructura como servicio que proporciona OpenStack. Está desarrollada con Django, integrando el sistema de ejecución de algoritmos en el backend de la aplicación. P-3CO utiliza diferentes tecnologías: C, Python, Bash scripting, HTML, CSS y Javascript. La mezcla de estas tecnologías permite obtener un software flexible, capaz de ejecutar software paralelo que utiliza distintas formas de paralelizar el software, como pueden ser OpenMP y MPI.

## Características
- **Análisis de Costes:** Ofrece una visión detallada del coste estimado de ejecutar un programa en una instancia específica, ayudando a tomar decisiones informadas sobre la infraestructura de ejecución.
- **Interfaz Intuitiva:** La interfaz de usuario de P-3CO es fácil de usar y proporciona visualizaciones claras de los datos de estimación y análisis.

## Estructura del repositorio
- **Carpeta c:** Contiene algoritmos del Juego de la Vida con MPI, OpenMP para probar el sistema.
- **Carpeta web:** Contiene la aplicación web en Django.

## Instalación
1. Crea una instancia Debian 11 en el usuario de OpenStack que tengas disponible.
2. Conecta una terminal a la instancia.
3. Ejecuta el script de instalación webServer.sh en la instancia (Puede ser necesario actualizar los permisos del script).

## Puesta en marcha
1. Ejecuta la aplicación en la instancia utilizando los siguientes comandos:
    ```bash
    source venv/bin/activate
    cd TFGinformaticaWeb/web
    python manage.py runserver 0.0.0.0:8080
    // Si se desea mantener el servidor levantado sustituir la última instrucción por: nohup python manage.py runserver 0.0.0.0:8080 &
    ```
