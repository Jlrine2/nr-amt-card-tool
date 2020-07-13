from os import environ

from boto3.dynamodb.conditions import Key

from amtcard_api import connexion_app
import boto3

PRIMARY_KEY = 'card_id'

DB = boto3.resource('dynamodb', region_name='us-west-2')


def register_user(body):
    table = DB.Table(environ['TABLE_NAME'])
    table.put_item(body)


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


def get_user(card_id):
    table = DB.Table(environ['TABLE_NAME'])
    key_expression = Key('card_id').eq(card_id)
    response = table.query(
        IndexName='card_id',
        KeyConditionExpression=key_expression
    )
    return response['Items']


connexion_app.add_api('openapi-spec.yml', validate_responses=True, strict_validation=True)
