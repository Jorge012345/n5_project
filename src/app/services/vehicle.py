import boto3
import shortuuid
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from src.app import schemas

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Vehicle")


class Vehicle:
    @staticmethod
    def create_vehicle(vehicle: schemas.Vehicle):
        vehicle.vehicle_id = f"vehicle_{shortuuid.uuid()}"
        try:
            table.put_item(Item=vehicle.dict())
        except ClientError as e:
            raise Exception("Error creating vehicle: " + e.response["Error"]["Message"])

    @staticmethod
    def get_vehicle(vehicle_id: str):
        try:
            response = table.get_item(Key={"vehicle_id": vehicle_id})
            return response.get("Item")
        except ClientError as e:
            raise Exception("Error getting vehicle: " + e.response["Error"]["Message"])

    @staticmethod
    def update_vehicle(vehicle_id: str, vehicle: schemas.Vehicle):
        update_expression = "SET license_plate = :license_plate, brand = :brand, color = :color, person_id = :person_id"
        expression_attribute_values = {
            ":license_plate": vehicle.license_plate,
            ":brand": vehicle.brand,
            ":color": vehicle.color,
            ":person_id": vehicle.person_id,
        }

        try:
            response = table.update_item(
                Key={"vehicle_id": vehicle_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression="attribute_exists(vehicle_id)",  # Asegura que el item exista
                ReturnValues="UPDATED_NEW",  # Opcional: devuelve los valores actualizados
            )
            return schemas.Vehicle(**response.get("Attributes"))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "ConditionalCheckFailedException":
                return "ConditionalCheckFailedException"
            else:
                raise Exception(
                    "Error updating vehicle: " + e.response["Error"]["Message"]
                )

    @staticmethod
    def delete_vehicle(vehicle_id: str):
        try:
            table.delete_item(
                Key={"vehicle_id": vehicle_id},
                ConditionExpression="attribute_exists(vehicle_id)",  # Asegura que el ítem exista
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ConditionalCheckFailedException":
                return "ConditionalCheckFailedException"
            else:
                raise Exception(
                    "Error deleting vehicle: " + e.response["Error"]["Message"]
                )

    @staticmethod
    def get_vehicle_by_license_plate(license_plate: str):
        try:
            response = table.scan(
                FilterExpression=Attr("license_plate").eq(license_plate)
            )
            items = response.get("Items", [])
            return items[0] if items else None
        except ClientError as e:
            raise Exception("Error getting vehicle: " + e.response["Error"]["Message"])

    @staticmethod
    def get_all_vehicles():
        try:
            response = table.scan()
            return response.get("Items", [])
        except ClientError as e:
            raise Exception(
                "Error retrieving vehicles: " + e.response["Error"]["Message"]
            )

    @staticmethod
    def get_vehicles_by_person_id(person_id: str):
        try:
            response = table.scan(FilterExpression=Attr("person_id").eq(person_id))
            items = response.get("Items", [])
            return [schemas.Vehicle(**item) for item in items] if items else None
        except ClientError as e:
            raise Exception("Error getting vehicles: " + e.response["Error"]["Message"])
