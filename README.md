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

    # Inicia DynamoDB local en Docker
    docker run -p 8000:8000 amazon/dynamodb-local

    # Crea la tabla en DynamoDB local
    aws dynamodb create-table --cli-input-json file://create-table.json --endpoint-url http://localhost:8000
    ```
4. DynamoDB local debería estar en funcionamiento en tu computadora local en http://localhost:8000. Puedes acceder a la consola de administración de DynamoDB local en un navegador web visitando http://localhost:8000/shell.
5. Ahora puedes desarrollar y probar tu aplicación utilizando DynamoDB local como si fuera una base de datos en AWS.
6. Cuando hayas terminado de usar DynamoDB local, puedes detener el contenedor de Docker presionando **Ctrl + C** en la terminal donde se está ejecutando.

¡Eso es todo! Ahora tienes DynamoDB local ejecutándose en tu computadora macOS a través de Docker, lo que te permite desarrollar y probar aplicaciones que utilizan DynamoDB sin necesidad de una conexión a AWS. Ten en cuenta que DynamoDB local es solo para desarrollo y pruebas locales; no se recomienda su uso en producción.

## Prompt - 2: Creación de interfaz para consultas a Base de Datos DynamoDB

**Prompt**: *Asume que eres un experto en python, en diseño de interfaces y en bases de datos NoSQL como DynamoDB.*

*Quiero construir una interfaz grafica en python que me permita, de forma visual, hacer consultas a una base de datos de DynamoDB, para empezar específicame que paquetes necesito instalar para poder crear interfaces, y dame un ejemplo de una interfaz básica en la que pueda seleccionar la tabla a la cual le quiero hacer la consulta. Para esto incluye una forma en la que me pueda conectar con la base de datos de AWS DynamoDB asumiendo que tengo el Access Key ID y el Secret Access Key*

**Respuesta**: Para construir una interfaz gráfica en Python que te permita hacer consultas visuales a una base de datos DynamoDB, puedes utilizar la biblioteca tkinter para la creación de la interfaz y la biblioteca boto3 para interactuar con DynamoDB. Asegúrate de que ambos paquetes estén instalados en tu entorno de Python.

Primero, necesitas instalar los paquetes si aún no los tienes instalados. Puedes hacerlo utilizando pip:

```bash
pip install tkinter
pip install boto3
```
Luego, puedes crear una interfaz gráfica básica que te permita seleccionar la tabla de DynamoDB y realizar consultas. Aquí tienes un ejemplo simple:
```python
import tkinter as tk
from tkinter import ttk
import boto3

# Configura las credenciales de AWS
access_key = 'YOUR_ACCESS_KEY'
secret_key = 'YOUR_SECRET_KEY'
region = 'us-east-1'  # Reemplaza con tu región de AWS

# Inicializa el cliente de DynamoDB
dynamodb = boto3.client('dynamodb', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

# Función para realizar una consulta en la tabla seleccionada
def execute_query():
    table_name = table_combobox.get()
    query_result.delete(1.0, tk.END)  # Borra el resultado anterior
    query_result.insert(tk.END, f"Consultando la tabla: {table_name}\n\n")

    # Aquí puedes agregar tu lógica de consulta a DynamoDB
    # Por ejemplo, puedes usar el método query o scan de DynamoDB
    # y mostrar los resultados en la caja de texto.

    # Ejemplo simple de consulta (reemplaza con tu propia lógica):
    response = dynamodb.scan(TableName=table_name)
    for item in response['Items']:
        query_result.insert(tk.END, f"{item}\n")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Consultas a DynamoDB")

# Etiqueta de selección de tabla
table_label = tk.Label(root, text="Selecciona la tabla:")
table_label.pack()

# ComboBox para seleccionar la tabla
table_options = ["Table1", "Table2", "Table3"]  # Reemplaza con tus nombres de tablas
table_combobox = ttk.Combobox(root, values=table_options)
table_combobox.pack()

# Botón para ejecutar la consulta
query_button = tk.Button(root, text="Ejecutar Consulta", command=execute_query)
query_button.pack()

# Cuadro de texto para mostrar el resultado de la consulta
query_result = tk.Text(root, height=10, width=40)
query_result.pack()

root.mainloop()
```

Asegúrate de reemplazar **'YOUR_ACCESS_KEY'** y **'YOUR_SECRET_KEY'** con tus propias credenciales de AWS. También, reemplaza table_options con los nombres de tus tablas en DynamoDB.

Este es un ejemplo muy básico, y deberás personalizarlo para que se ajuste a tus necesidades específicas de consulta y diseño de interfaz. Puedes agregar más funcionalidades y características a medida que lo necesites.

**Prompt**: *Modifica el código para que pueda incluir un endpoint url donde está ubicada la base de datos de Dynamo, ademas, haz que la lista de tablas se consulte directamente en la base de datos antes de desplegarla*

**Respuesta**: Para conectarte a una base de datos de DynamoDB, debes proporcionar el punto final (endpoint URL) en lugar de las credenciales de acceso y la región. También puedes utilizar la biblioteca boto3 para listar las tablas en la base de datos. A continuación, se muestra el código modificado para incluir el punto final y obtener la lista de tablas desde DynamoDB:
```python
# Configura el punto final de DynamoDB
dynamodb_endpoint = 'https://your-dynamodb-endpoint-url'  # Reemplaza con tu punto final de DynamoDB

# Inicializa el cliente de DynamoDB
dynamodb = boto3.client('dynamodb', endpoint_url=dynamodb_endpoint)

# Función para obtener la lista de tablas
def get_table_names():
    table_names = []
    response = dynamodb.list_tables()
    table_names = response['TableNames']
    return table_names

...
...
...

# ComboBox para seleccionar la tabla
table_options = get_table_names()
table_combobox = ttk.Combobox(root, values=table_options)
table_combobox.pack()
````
Asegúrate de reemplazar **'https://your-dynamodb-endpoint-url'** con el punto final de tu base de datos DynamoDB. La función get_table_names obtendrá la lista de tablas desde DynamoDB y la usará para llenar el ComboBox.

Este código debería permitirte seleccionar una tabla de DynamoDB desde una lista generada dinámicamente a partir de la base de datos y ejecutar consultas en la tabla seleccionada.