import json
import boto3
import os

# Initialiser DynamoDB avec la variable d'environnement
dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        print("Event reçu :", event)

        # Récupération et parsing du body
        if "body" in event:
            if isinstance(event["body"], str):
                body = json.loads(event["body"])
            else:
                body = event["body"]
        else:
            body = event

        todo_id = body.get("id")
        if not todo_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "L'ID de la tâche est requis"})
            }

        # Construire dynamiquement l'UpdateExpression
        update_expression_parts = []
        expression_attribute_names = {}
        expression_attribute_values = {}

        for key, value in body.items():
            if key != "id" and value is not None:
                placeholder_name = f"#{key}"
                placeholder_value = f":{key}"
                update_expression_parts.append(f"{placeholder_name} = {placeholder_value}")
                expression_attribute_names[placeholder_name] = key
                expression_attribute_values[placeholder_value] = value

        if not update_expression_parts:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Aucun champ à mettre à jour"})
            }

        update_expression = "SET " + ", ".join(update_expression_parts)

        # Mettre à jour l'élément dans DynamoDB
        response = table.update_item(
            Key={"id": todo_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Tâche mise à jour",
                "item": response.get("Attributes", {})
            })
        }

    except Exception as e:
        print("Erreur :", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


#test labda code
{
  "id": "1ec8aace-9835-4171-95de-6e9aa7b56876",
  "title": "test update",
  "status": "completed"
}
