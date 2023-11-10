import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY")


def generate_dynamodb_query(question: str):
    client = OpenAI(api_key=api_key)
    gpt3_answer = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en crear FilterExpressions para DynamoDB haciendo uso de boto3 en python, para ello, cada que te pregunte algo, respondeme con el FilterExpression que necesito sin formato de código, un separador y los nombre y valores para el ExpressionAttributeValues y un separador luego con los keys y nombres para el ExpressionAttributesNames. Los campos de la tabla que se consulta son: payment_id, date, amount, card, merchant_id y status; date es un timestamp en segundos, cuando recibas una fecha, conviertela a este formato de timestamp",
            },
            {
                "role": "user",
                "content": "Dame las ventas realizadas por el merchant MERCHANT123 entre el 1 de octubre y el 5 de noviembre del 2023",
            },
            {
                "role": "assistant",
                "content": "#merchant_id = :merchant_id AND #fecha BETWEEN :date_ini and :date_end separador {':merchant_id': {'S': 'MERCHANT123'}, ':date_ini': {'N': '1696136400'}, ':date_end': {'N': '1699160400'}} separador {'#merchant_id': 'merchant_id', '#fecha': 'date'}",
            },
            {
                "role": "user",
                "content": "Dame las ventas del día 2 de octubre del 2022",
            },
            {
                "role": "assistant",
                "content": "#fecha = :date separador {':date': {'N': '1664668800'}} separador {'#fecha': 'date'}",
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

    print(query_dynamo)
    filter_expression, attribute_values, attribute_names = query_dynamo.split(
        "separador"
    )
    attribute_values = json.loads(attribute_values.replace("'", '"'))
    attribute_names = json.loads(attribute_names.replace("'", '"'))
    print(filter_expression)
    print(attribute_values)
    print(attribute_names)
    return query_dynamo


question = "Dame las ventas del día 5 de octubre del 2022"
query = generate_dynamodb_query(question=question)
