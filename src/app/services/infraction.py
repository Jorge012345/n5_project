import boto3
import shortuuid
from botocore.exceptions import ClientError
from src.app import schemas
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Infraction")


class Infraction:
    @staticmethod
    def create_infraction(infraction: schemas.Infraction):
        infraction.infraction_id = f"infraction_{shortuuid.uuid()}"
        infraction.timestamp = datetime.now(timezone.utc).isoformat()

        try:
            table.put_item(Item=infraction.dict())
        except ClientError as e:
            raise Exception(
                "Error creating infraction: " + e.response["Error"]["Message"]
            )

    @staticmethod
    def get_infractions_by_license_plates(license_plates: list):

        try:
            response = table.scan(
                FilterExpression=Attr("license_plate").is_in(license_plates)
            )
            items = response.get("Items", [])
            return [schemas.Infraction(**item) for item in items]
        except ClientError as e:
            raise Exception(
                "Error getting infractions: " + e.response["Error"]["Message"]
            )
