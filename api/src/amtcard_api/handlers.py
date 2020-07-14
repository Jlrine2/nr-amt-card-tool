from os import environ

from connexion import problem
from flask_cors import CORS

from amtcard_api import connexion_app
import boto3

PRIMARY_KEY = 'card_id'

DB = boto3.resource('dynamodb', region_name='us-west-2')


def register_user(body):
    table = DB.Table(environ['TABLE_NAME'])
    table.put_item(Item=body)
    return {'user_added': body}


def update_user(body):
    table = DB.Table(environ['TABLE_NAME'])
    key = {PRIMARY_KEY: body[PRIMARY_KEY]}
    update_expression = 'SET {}'.format(','.join(f'{k}=:{k}' for k in body if k != PRIMARY_KEY))
    expression_attribute_values = {f':{k}': v for k, v in body.items() if k != PRIMARY_KEY}
    table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return {'user_updated': body}


def get_user(card_id):
    table = DB.Table(environ['TABLE_NAME'])
    key = {'card_id': card_id}
    response = table.get_item(
        Key=key
    )
    if "Item" not in response:
        return problem(400, "BadRequest", "Card Id does not exist")
    return response['Item']


connexion_app.add_api('openapi-spec.yml', validate_responses=True, strict_validation=True)
CORS(connexion_app.app, supports_credentials=True)
