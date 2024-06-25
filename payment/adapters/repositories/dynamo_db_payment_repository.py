"""
This module contains the implementation of the DynamoDB payment repository.
"""
import os
from datetime import datetime
import boto3

class DynamoDBPaymentRepository:
    """
    This class implements the DynamoDB payment repository.
    """
    def __init__(self):
        """
        This method initializes the DynamoDB payment repository.
        """
        self.client = boto3.client("dynamodb")
        self.table_name = f"{os.environ.get('TABLE_NAME')}-dev"

    def create(self, payment: dict):
        """
        This method creates a new payment.
        """
        pass

    def get_payment_by_idempotency_key(self, idempotency_key: str) -> dict:
        """
        This method retrieves a payment by its idempotency key.
        """
        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                "idempotency_key": {"S": idempotency_key}
            }
        )

        item = response["Item"]

        return self.transform_payment_to_prettified_response(item)

    def transform_payment_to_prettified_response(self, payment: dict) -> dict:
        """
        This method transforms a payment to a prettified dictionary response.
        """
        prettified_response = {
            "idempotency_key": payment["idempotency_key"]["S"],
            "payment_id": payment["payment_id"]["N"],
            "status": payment["status"]["S"],
            "order_id": payment["order_id"]["N"],
            "external_id": payment["external_id"]["N"],
            "vehicle_id": payment["vehicle_id"]["N"],
            "created_at": payment["created_at"]["S"],
            "updated_at": payment["updated_at"]["S"],
        }

        return prettified_response

    def store_payment(self, payment: dict):
        """
        This method stores a payment.
        """
        self.client.put_item(
            TableName=self.table_name,
            Item={
                "idempotency_key": {"S": str(payment["idempotency_key"])},
                "status": {"S": payment["status"]},
                "order_id": {"N": str(payment["order_id"])},
                "payment_id": {"N": str(payment["payment_id"])},
                "external_id": {"N": str(payment["external_id"])},
                "vehicle_id": {"N": str(payment["vehicle_id"])},
                "created_at": {"S": datetime.now().isoformat()},
                "updated_at": {"S": datetime.now().isoformat()}
            }
        )
