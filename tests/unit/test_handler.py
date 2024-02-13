import os

import boto3
import moto
import pytest
from handler import increment_count, lambda_handler


# ===============================================================
# Fixtures
# ===============================================================
@pytest.fixture(scope="session")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"  # noqa
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # noqa
    os.environ["AWS_SECURITY_TOKEN"] = "testing"  # noqa
    os.environ["AWS_SESSION_TOKEN"] = "testing"  # noqa
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def dynamodb_client(aws_credentials):
    """Mocked DynamoDB client."""
    with moto.mock_dynamodb():
        yield boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="function")
def dynamodb_table(dynamodb_client):
    # os.environ["HITS_TABLE_NAME"] = "hits"  # noqa set in pytest.ini
    dynamodb_client.create_table(
        TableName="hits",
        KeySchema=[
            {"AttributeName": "path", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "path", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    yield dynamodb_client
    dynamodb_client.delete_table(TableName="hits")


# ===============================================================
# Tests
# ===============================================================
def test_increment_counter_zero(dynamodb_table):
    """
    Test that the counter is incremented to 1 when it is not initialized.
    """
    count = increment_count()
    assert count == 1

    response = dynamodb_table.get_item(
        TableName="hits", Key={"path": {"S": "hit_count"}}
    )
    assert response["Item"]["h_count"]["N"] == "1"


def test_increment_counter_notzero(dynamodb_table):
    """
    Test that the counter is incremented to 1 more than the current setting.
    """
    # initialize the hit counter to 7
    dynamodb_table.put_item(
        TableName="hits",
        Item={
            "path": {"S": "hit_count"},
            "h_count": {"N": "7"},
            "h_date": {"S": "2021-01-01"},
            "h_time": {"S": "12:00:00"},
            "h_ip": {"S": "127.0.0.1"},
        },
    )

    count = increment_count()
    assert count == 8

    response = dynamodb_table.get_item(
        TableName="hits", Key={"path": {"S": "hit_count"}}
    )
    assert response["Item"]["h_count"]["N"] == "8"


def test_lambda_handler_zero(dynamodb_table):
    # call the lambda handler function
    response = lambda_handler({}, {})
    # assert that the response is a success
    assert response["statusCode"] == 200
    # assert that the response contains the expected message
    assert response["body"] == '{"count": 1}'


def test_lambda_handler_notableenvset(dynamodb_table):
    # test that the HITS_TABLE_NAME environment variable is set
    # throws an error if it is not set.
    del os.environ["HITS_TABLE_NAME"]
    with pytest.raises(Exception) as excinfo:
        lambda_handler({}, {})

    assert "HITS_TABLE_NAME environment variable not set" in str(excinfo.value)
    # reset the environment variable
    os.environ["HITS_TABLE_NAME"] = "hits"
