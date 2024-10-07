import boto3
import shortuuid
from botocore.exceptions import ClientError
from src.app import schemas
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Officer")


class Officer:
    @staticmethod
    def create_officer(officer: schemas.Officer):
        officer.officer_id = f"officer_{shortuuid.uuid()}"
        try:
            table.put_item(Item=officer.dict())
        except ClientError as e:
            raise Exception("Error creating officer: " + e.response["Error"]["Message"])

    @staticmethod
    def get_officer(officer_id: str):
        try:
            response = table.get_item(Key={"officer_id": officer_id})
            
            return response.get("Item")
        except ClientError as e:
            raise Exception("Error getting officer: " + e.response["Error"]["Message"])
        except Exception as e:
            print("....Exception: ",e)
    @staticmethod
    def update_officer(officer_id: str, officer: schemas.Officer):
        update_expression = "SET #name = :name, identification = :identification"
        expression_attribute_names = {"#name": "name"}
        expression_attribute_values = {
            ":name": officer.name,
            ":identification": officer.identification,
        }

        try:
            response = table.update_item(
                Key={"officer_id": officer_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression="attribute_exists(officer_id)",  # Asegura que el item exista
                ReturnValues="UPDATED_NEW",  # Opcional: devuelve los valores actualizados
            )
            return schemas.Officer(**response.get("Attributes"))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "ConditionalCheckFailedException":
                return "ConditionalCheckFailedException"
            else:
                raise Exception(
                    "Error updating officer: " + e.response["Error"]["Message"]
                )

    @staticmethod
    def delete_officer(officer_id: str):
        try:
            table.delete_item(
                Key={"officer_id": officer_id},
                ConditionExpression="attribute_exists(officer_id)",  # Asegura que el ítem exista
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ConditionalCheckFailedException":
                return "ConditionalCheckFailedException"
            else:
                raise Exception(
                    "Error deleting officer: " + e.response["Error"]["Message"]
                )

    @staticmethod
    def get_all_officers():
        try:
            response = table.scan()
            return response.get("Items", [])
        except ClientError as e:
            raise Exception(
                "Error retrieving officers: " + e.response["Error"]["Message"]
            )

    @staticmethod
    def get_officer_by_identification(identification: str):
        try:
            response = table.scan(
                FilterExpression=Attr("identification").eq(identification)
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except ClientError as e:
            raise Exception("Error getting vehicle: " + e.response["Error"]["Message"])
