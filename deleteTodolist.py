import json
import boto3
import os
from botocore.exceptions import ClientError

# ⚡ Nom de la table DynamoDB depuis la variable d'environnement
TABLE_NAME = os.environ.get("TABLE_NAME")

# Client DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        # API Gateway passe le body en JSON string → on le parse
        body = json.loads(event.get("body", "{}"))

        # Vérifier que "id" est fourni
        if "id" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'id' parameter"})
            }

        item_id = body["id"]

        # Suppression de l’élément dans DynamoDB
        response = table.delete_item(
            Key={
                "id": item_id
            },
            ConditionExpression="attribute_exists(id)"  # évite de supprimer un id inexistant
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Item with id {item_id} deleted successfully",
                "response": str(response)
            })
        }

    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Item with id {body['id']} not found"})
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
#Test delete

{
  "body": "{\"id\": \"1ec8aace-9835-4171-95de-6e9aa7b56876\"}"
}
