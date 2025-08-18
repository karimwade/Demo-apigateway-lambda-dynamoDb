import json
import boto3
import os
import uuid

# Initialiser le client DynamoDB avec variable d'environnement
dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TABLE_NAME"]  # On force la présence de la variable
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        print("Event reçu :", event)

        # Vérification et parsing du body
        if "body" in event:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        else:
            body = event  # Appel direct en dict (ex: test Lambda)

        # Validation des champs requis
        title = body.get("title")
        if not title:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Title is required"})
            }

        # Création de l'item
        todo_id = str(uuid.uuid4())
        item = {
            "id": todo_id,
            "title": title,
            "status": body.get("status", "pending")
        }

        # Insertion dans DynamoDB
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Tâche ajoutée",
                "item": item
            })
        }

    except Exception as e:
        print("Erreur :", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }




# Test aws labda
# nom table : TodoTable

{
  "body": "{\"title\": \"Test depuis Lambda\", \"status\": \"pending\"}"
}

