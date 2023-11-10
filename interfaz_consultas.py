import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk

import boto3
from dotenv import load_dotenv
from openai import OpenAI
from prettytable import PrettyTable

load_dotenv()

api_key = os.getenv("API_KEY")

# Configura el punto final de DynamoDB
dynamodb_endpoint = "http://localhost:8000"  # Reemplaza con tu punto final de DynamoDB

# Configura las credenciales de AWS
access_key = "DUMMYIDEXAMPLE"
secret_key = "DUMMYEXAMPLEKEY"
region = "us-east-1"  # Reemplaza con tu región de AWS

# Inicializa el cliente de DynamoDB
dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=dynamodb_endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region,
)


# Función para convertir una fecha a un timestamp UNIX en segundos
def convert_to_unix_timestamp(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        timestamp = int(date.timestamp())
        return timestamp
    except ValueError:
        return None


# Lenguaje natural a consulta de dynamo
def generate_dynamodb_query(question: str):
    client = OpenAI(api_key=api_key)
    gpt3_answer = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en crear FilterExpressions para DynamoDB haciendo uso de boto3 en python, para ello, cada que te pregunte algo, respondeme con el FilterExpression que necesito sin formato de código, un separador y los nombre y valores para el ExpressionAttributeValues y un separador luego con los keys y nombres para el ExpressionAttributesNames. Los campos de la tabla que se consulta son: payment_id, date, amount, card, merchant_id y status; cuando recibas una fecha, conviertela a este formato YYYY-MM-DD",
            },
            {
                "role": "user",
                "content": "Dame las ventas realizadas por el merchant MERCHANT123 entre el 1 de octubre y el 5 de noviembre del 2023",
            },
            {
                "role": "assistant",
                "content": "#merchant_id = :merchant_id AND #fecha BETWEEN :date_ini and :date_end separador {':merchant_id': {'S': 'MERCHANT123'}, ':date_ini': {'N': '2023-10-01'}, ':date_end': {'N': '2023-11-05'}} separador {'#merchant_id': 'merchant_id', '#fecha': 'date'}",
            },
            {
                "role": "user",
                "content": "Dame las ventas del día 2 de octubre del 2022",
            },
            {
                "role": "assistant",
                "content": "#fecha = :date separador {':date': {'N': '2022-10-02'}} separador {'#fecha': 'date'}",
            },
            {"role": "user", "content": "Dame las ventas mayores a 50000"},
            {
                "role": "assistant",
                "content": "#cantidad > :amount separador {':amount': {'N': '50000'}} separador {'#cantidad': 'amount'}",
            },
            {"role": "user", "content": question},
        ],
    )

    query_dynamo = gpt3_answer.choices[0].message.content

    filter_expression, attribute_values, attribute_names = query_dynamo.split(
        "separador"
    )
    attribute_values = json.loads(attribute_values.replace("'", '"'))
    attribute_names = json.loads(attribute_names.replace("'", '"'))

    if "fecha" in filter_expression:
        if attribute_values.get(":date", None):
            attribute_values[":date"]["N"] = str(
                convert_to_unix_timestamp(attribute_values[":date"]["N"])
            )
        if attribute_values.get(":date_ini", None):
            attribute_values[":date_ini"]["N"] = str(
                convert_to_unix_timestamp(attribute_values[":date_ini"]["N"])
            )
        if attribute_values.get(":date_end", None):
            attribute_values[":date_end"]["N"] = str(
                convert_to_unix_timestamp(attribute_values[":date_end"]["N"])
            )

    return filter_expression, attribute_values, attribute_names


# Función para obtener la lista de tablas
def get_table_names():
    table_names = []
    response = dynamodb.list_tables()
    table_names = response["TableNames"]
    return table_names


# Función para realizar una consulta en la tabla seleccionada
def execute_query():
    table_name = table_combobox.get()
    consulta = consulta_entry.get()

    filter_expression, attribute_values, attribute_names = generate_dynamodb_query(
        consulta
    )

    query_log_text.delete(1.0, tk.END)  # Borra los logs anteriores
    query_log_text.insert(tk.END, "Realizando consulta...\n")
    query_log_text.insert(tk.END, f"Consultando la tabla: {table_name}\n")
    query_log_text.insert(tk.END, f"Consulta: {filter_expression}\n\n")

    # Aquí puedes agregar tu lógica de consulta a DynamoDB utilizando la consulta
    # Por ejemplo, puedes usar el método query o scan de DynamoDB y mostrar los resultados en la caja de texto.

    # Ejemplo simple de consulta (reemplaza con tu propia lógica):
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression=filter_expression,
        ExpressionAttributeValues=attribute_values,
        ExpressionAttributeNames=attribute_names,
    )
    # Configuración de la tabla
    columns = list(response["Items"][0].keys())
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Configuración de las columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(
            col, width=150
        )  # Ajusta el ancho de las columnas según sea necesario

    # Llena la tabla con los datos
    for item in response["Items"]:
        tree.insert("", "end", values=list(item.values()))

    # Muestra la tabla
    tree.pack()

    query_log_text.insert(tk.END, "Consulta finalizada.\n")


# Configuración de la ventana principal
root = tk.Tk()
root.title("Consultas a DynamoDB")

# Etiqueta de selección de tabla
table_label = tk.Label(root, text="Selecciona la tabla:")
table_label.pack()

# ComboBox para seleccionar la tabla
table_options = get_table_names()
table_combobox = ttk.Combobox(root, values=table_options)
table_combobox.pack()

# Etiqueta y entrada para la consulta
consulta_label = tk.Label(root, text="Consulta:")
consulta_label.pack()
consulta_entry = ttk.Entry(root, width=100)
consulta_entry.pack()

# Botón para ejecutar la consulta
query_button = tk.Button(root, text="Ejecutar Consulta", command=execute_query)
query_button.pack()

# Cuadro de texto para mostrar mensajes de log
query_log_label = tk.Label(root, text="Log de consulta:")
query_log_label.pack()
query_log_text = tk.Text(root, height=10, width=40)
query_log_text.pack()

root.mainloop()
