from datetime import datetime, timedelta
from json import dumps

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parameters import get_parameter
from boto3 import client
from jwt import decode, encode
from jwt.exceptions import DecodeError

from common import get_required_var


logger = Logger()


def contact_from_body(body):
    if "sms" in body:
        contact_type = "sms"
        contact_value = body["sms"]
    elif "email" in body:
        contact_type = "email"
        contact_value = body["email"]
    return contact_type, contact_value


def gen_key(contact_type: str, contact_value: str, code: str):
    return f"{contact_type}:{contact_value}:{code}"


def put_item(contact_type: str, contact_value: str, code: str):
    table_name = get_required_var("AUTH_TABLE_NAME")
    item = {
        "auth": {"S": gen_key(contact_type, contact_value, code)},
        "ttl": {"N": str(int((datetime.utcnow() + timedelta(minutes=15)).timestamp()))},
        "iat": {"N": str(int(datetime.utcnow().timestamp()))},
    }
    logger.debug(f"Putting DynamoDB Item table: {table_name}; item: {dumps(item)}.")

    resp = client("dynamodb").put_item(
        TableName=table_name,
        Item=item,
    )
    logger.debug(f"Put DynamoDB Item response: {dumps(resp)}.")


def check_item(contact_type: str, contact_value: str, code: str):
    table_name = get_required_var("AUTH_TABLE_NAME")
    item_key = gen_key(contact_type, contact_value, code)
    logger.debug(f"Getting DynamoDB Item table: {table_name}; item_key: {item_key}.")

    resp = client("dynamodb").get_item(
        TableName=table_name,
        Key={"auth": {"S": item_key}},
        ConsistentRead=True,
    )
    logger.debug(f"Get DynamoDB Item response: {dumps(resp)}.")

    return True if "Item" in resp else False


def delete_item(contact_type: str, contact_value: str, code: str):
    table_name = get_required_var("AUTH_TABLE_NAME")
    item_key = gen_key(contact_type, contact_value, code)
    logger.debug(f"Deleting DynamoDB Item table: {table_name}; item_key: {item_key}.")

    resp = client("dynamodb").delete_item(
        TableName=table_name,
        Key={"auth": {"S": item_key}},
    )
    logger.debug(f"Deleted DynamoDB Item response: {dumps(resp)}.")


def encode_token(remember: bool):
    secret_token = get_parameter(get_required_var("SECRET_TOKEN_PARAM_NAME"), decrypt=True)
    exp_hours = 365 * 24 if remember else 1
    context = {
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(hours=exp_hours)).timestamp()),
    }
    return encode(context, secret_token, algorithm="HS256")


def check_token(token):
    secret_token = get_parameter(get_required_var("SECRET_TOKEN_PARAM_NAME"), decrypt=True)
    try:
        context = decode(token, secret_token, algorithms=["HS256"])
        return context.get("exp") > datetime.utcnow().timestamp()
    except DecodeError:
        return False


def send_message(contact_type: str, contact_value: str, message: str):
    if contact_type == "sms":
        if contact_value.startswith("+44"):
            region = "eu-west-2"
        elif contact_value.startswith("+55"):
            region = "sa-east-1"
        else:
            region = "us-east-1"
        logger.debug(f"Publishing SNS region: {region}; phone_number: {contact_value}; message: {message}.")

        resp = client("sns", region_name=region).publish(
            PhoneNumber=contact_value,
            Message=message,
        )
        logger.debug(f"Publish SNS response: {dumps(resp)}.")
    
    elif contact_type == "email":
        source = get_required_var("SOURCE_EMAIL")
        subject = "Brief Box"
        logger.debug(f"Sending Email source: {source}; to: {contact_value}; subject: {subject}; message: {message}.")

        resp = client("ses").send_email(
            Source=source,
            Destination={"ToAddresses": [contact_value]},
            Message={
                "Subject": {"Data": subject, "Charset": "utf-8"},
                "Body": {"Text": {"Data": message, "Charset": "utf-8"}},
            },
        )
        logger.debug(f"Sent Email response: {dumps(resp)}.")
