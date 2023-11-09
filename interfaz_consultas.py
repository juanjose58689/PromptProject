import tkinter as tk
from tkinter import ttk
import boto3
from datetime import datetime
import calendar

# Configura el punto final de DynamoDB
dynamodb_endpoint = 'http://localhost:8000'  # Reemplaza con tu punto final de DynamoDB

# Configura las credenciales de AWS
access_key = 'DUMMYIDEXAMPLE'
secret_key = 'DUMMYEXAMPLEKEY'
region = 'us-east-1'  # Reemplaza con tu región de AWS

# Inicializa el cliente de DynamoDB
dynamodb = boto3.client('dynamodb', endpoint_url=dynamodb_endpoint, aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

# Función para obtener la lista de tablas
def get_table_names() -> list:
    table_names = []
    response = dynamodb.list_tables()
    table_names = response['TableNames']
    return table_names

# Función para convertir una fecha a un timestamp UNIX en segundos
def convert_to_unix_timestamp(date_str: str) -> int:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        timestamp = int(date.timestamp())
        return timestamp
    except ValueError:
        return -1

# Función para realizar una consulta en la tabla seleccionada
def execute_query():
    table_name = table_combobox.get()
    payment_id = payment_id_entry.get()
    date = date_entry.get()
    
    # Convierte la fecha a un timestamp UNIX en segundos
    date_unix = convert_to_unix_timestamp(date)
    
    query_log_text.delete(1.0, tk.END)  # Borra los logs anteriores
    query_result_text.delete(1.0, tk.END)  # Borra el resultado anterior
    query_log_text.insert(tk.END, "Realizando consulta...\n")
    
    if date_unix != -1:
        query_log_text.insert(tk.END, f"Consultando la tabla: {table_name}\n")
        query_log_text.insert(tk.END, f"Payment ID: {payment_id}\n")
        query_log_text.insert(tk.END, f"Date (UNIX timestamp): {date_unix}\n\n")
        
        # Aquí puedes agregar tu lógica de consulta a DynamoDB utilizando payment_id y date_unix
        # Por ejemplo, puedes usar el método query o scan de DynamoDB
        # y mostrar los resultados en la caja de texto.

        # Ejemplo simple de consulta (reemplaza con tu propia lógica):
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression="#payment_id = :payment_id and #date = :date",
            ExpressionAttributeNames={
                "#payment_id": "payment_id",
                "#date": "date"
            },
            ExpressionAttributeValues={
                ":payment_id": {"S": payment_id},
                ":date": {"N": str(date_unix)}
            }
        )
        for item in response['Items']:
            query_result_text.insert(tk.END, f"{item}\n")
        
        query_log_text.insert(tk.END, "Consulta finalizada.\n")
    else:
        query_log_text.insert(tk.END, "Fecha no válida. Utiliza el formato 'YYYY-MM-DD'.\n")

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

# Etiqueta y entrada para el Payment ID
payment_id_label = tk.Label(root, text="Payment ID:")
payment_id_label.pack()
payment_id_entry = ttk.Entry(root)
payment_id_entry.pack()

# Etiqueta y entrada para la fecha (con selección de fecha)
date_label = tk.Label(root, text="Fecha (YYYY-MM-DD):")
date_label.pack()
date_entry = ttk.Entry(root)
date_entry.pack()

# Botón para ejecutar la consulta
query_button = tk.Button(root, text="Ejecutar Consulta", command=execute_query)
query_button.pack()

# Cuadro de texto para mostrar los resultados de la consulta
query_result_label = tk.Label(root, text="Resultado de la consulta:")
query_result_label.pack()
query_result_text = tk.Text(root, height=10, width=40)
query_result_text.pack()

# Cuadro de texto para mostrar mensajes de log
query_log_label = tk.Label(root, text="Log de consulta:")
query_log_label.pack()
query_log_text = tk.Text(root, height=10, width=40)
query_log_text.pack()

root.mainloop()
