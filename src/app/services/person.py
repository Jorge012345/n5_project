import boto3
import shortuuid
from botocore.exceptions import ClientError
from src.app import schemas
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Person")


class Person:
    @staticmethod
    def create_person(person: schemas.Person):
        person.person_id = f"person_{shortuuid.uuid()}"
        try:
            table.put_item(Item=person.dict())
        except ClientError as e:
            raise Exception("Error creating person: " + e.response["Error"]["Message"])

    @staticmethod
    def get_person(person_id: str):
        try:
            response = table.get_item(Key={"person_id": person_id})
            return response.get("Item")
        except ClientError as e:
            raise Exception("Error getting person: " + e.response["Error"]["Message"])

    @staticmethod
    def update_person(person_id: str, person: schemas.Person):
        update_expression = "SET #name = :name, email = :email"
        expression_attribute_names = {"#name": "name"}
        expression_attribute_values = {":name": person.name, ":email": person.email}

        try:
            response = table.update_item(
                Key={"person_id": person_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression="attribute_exists(person_id)",  # Asegura que el item exista
                ReturnValues="UPDATED_NEW",  # Opcional: devuelve los valores actualizados
            )
            return schemas.Person(**response.get("Attributes"))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "ConditionalCheckFailedException":
                return "ConditionalCheckFailedException"
            else:
                raise Exception(
                    "Error updating person: " + e.response["Error"]["Message"]
                )

    @staticmethod
    def delete_person(person_id: str):
        try:
            table.delete_item(
                Key={"person_id": person_id},
                ConditionExpression="attribute_exists(person_id)",  # Asegura que el ítem exista
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ConditionalCheckFailedException":
                return "ConditionalCheckFailedException"
            else:
                raise Exception(
                    "Error deleting person: " + e.response["Error"]["Message"]
                )

    @staticmethod
    def get_all_persons():
        try:
            response = table.scan()
            return response.get("Items", [])
        except ClientError as e:
            raise Exception(
                "Error retrieving persons: " + e.response["Error"]["Message"]
            )

    @staticmethod
    def get_person_by_email(email: str):
        try:
            response = table.scan(FilterExpression=Attr("email").eq(email))
            items = response.get("Items", [])
            return schemas.Person(**items[0]) if items else None
        except ClientError as e:
            raise Exception("Error getting person: " + e.response["Error"]["Message"])
