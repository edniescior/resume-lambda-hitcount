import json
import logging
import os
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from lambda_decorators import catch_errors, with_logging

log_level = os.getenv("LOG_LEVEL", "INFO")

logger = logging.getLogger()
logger.setLevel(log_level)

_dynamodb = None


def get_dynamodb() -> boto3.resource:
    global _dynamodb
    if _dynamodb is None:
        _dynamodb = boto3.resource("dynamodb")
    return _dynamodb


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def increment_count() -> int:
    """Increment the hit count"""
    hits_table = os.getenv("HITS_TABLE_NAME")
    if not hits_table:
        raise Exception("HITS_TABLE_NAME environment variable not set")

    # Increment the hit count of the path key in the DynamoDB table
    dynamodb = get_dynamodb()
    table = dynamodb.Table(hits_table)
    response = table.update_item(
        Key={"path": "hit_count"},
        UpdateExpression="ADD h_count :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )
    logger.debug(f"Response: {json.dumps(response, indent=2, cls=DecimalEncoder)}")
    count = int(response["Attributes"]["h_count"])
    logger.info(f"Hit count updated: {count}")
    return count


@with_logging
@catch_errors
def lambda_handler(event, context):

    # Increment the hit count
    count = increment_count()

    return {
        "statusCode": 200,
        "body": f'{{"count": {count}}}',
    }
