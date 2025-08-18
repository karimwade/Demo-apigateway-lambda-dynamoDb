import json
import boto3
import os

# Initialiser DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TABLE_NAME"]  # obligatoire, sinon erreur
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        print("Event reçu :", event)

        # Récupérer toutes les tâches
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Liste des tâches",
                "items": items
            })
        }

    except Exception as e:
        print("Erreur :", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# Test aws lambda
{
  "httpMethod": "GET"
}
