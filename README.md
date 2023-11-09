# PromptProject
Repositorio donde se almacena el trabajo final de la asignatura PROM del estudiante Juan José Sánchez Correa.

## Prompt - 1: Desplegar ambiente local de DynamoDB para pruebas

**Prompt**: *Necesito simular una base de datos de tipo DynamoDB en mi computador local, para esto me gustaría utilizar Docker con el fin de virtualizar el servicio y que lo pueda exportar de forma sencilla.*

*Asume que eres un experto en las tecnologías de AWS y de Docker:*
- *Dame un paso a paso detallado con el que podría hacer la instalación requerida en una computadora con sistema operativo macOS.*

**Respuesta**: Claro, puedo proporcionarte un paso a paso detallado para instalar y ejecutar DynamoDB localmente en tu computadora macOS utilizando Docker. DynamoDB Local es una versión emulada de Amazon DynamoDB que puedes utilizar para desarrollar y probar aplicaciones sin incurrir en costos de AWS. Aquí tienes los pasos:

**Requisitos previos:**

1. Asegúrate de tener Docker instalado en tu computadora. Puedes descargar Docker Desktop para macOS desde el sitio web de Docker: Descargar Docker Desktop.
2. Asegúrate de tener Homebrew instalado. Puedes instalarlo si aún no lo tienes con el siguiente comando:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```

**Pasos para instalar y ejecutar DynamoDB local con Docker:**

1. Abre la terminal en tu macOS.
2. Utiliza Homebrew para instalar la herramienta dynamodb-local de AWS CLI. Puedes instalarla con el siguiente comando:
    ```bash
    brew install awscli
    ```
3. Una vez que AWS CLI esté instalado, puedes usarlo para descargar y configurar DynamoDB local. Ejecuta los siguientes comandos:
    ```bash
    # Descarga DynamoDB local
    aws dynamodb create-table --generate-cli-skeleton > create-table.json

    # Edita create-table.json y ajusta las opciones de la tabla según tus necesidades

    # Crea la tabla en DynamoDB local
    aws dynamodb create-table --cli-input-json file://create-table.json --endpoint-url http://localhost:8000

    # Inicia DynamoDB local en Docker
    docker run -p 8000:8000 amazon/dynamodb-local
    ```
4. DynamoDB local debería estar en funcionamiento en tu computadora local en http://localhost:8000. Puedes acceder a la consola de administración de DynamoDB local en un navegador web visitando http://localhost:8000/shell.
5. Ahora puedes desarrollar y probar tu aplicación utilizando DynamoDB local como si fuera una base de datos en AWS.
6. Cuando hayas terminado de usar DynamoDB local, puedes detener el contenedor de Docker presionando **Ctrl + C** en la terminal donde se está ejecutando.

¡Eso es todo! Ahora tienes DynamoDB local ejecutándose en tu computadora macOS a través de Docker, lo que te permite desarrollar y probar aplicaciones que utilizan DynamoDB sin necesidad de una conexión a AWS. Ten en cuenta que DynamoDB local es solo para desarrollo y pruebas locales; no se recomienda su uso en producción.