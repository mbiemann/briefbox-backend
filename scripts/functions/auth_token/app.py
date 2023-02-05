from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

from auth import check_item, contact_from_body, encode_token, delete_item, send_message
from common import response


logger = Logger()


@logger.inject_lambda_context(log_event=True)
@event_source(data_class=APIGatewayProxyEventV2)
def handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> dict:
    try:
        body = event.json_body
        contact_type, contact_value = contact_from_body(body)
        code = body["code"]
        remember = "remember" in body and body["remember"] == "Y"

        if not check_item(contact_type, contact_value, code):
            return response(400, {"message": "Code is invalid."}, event.raw_event)

        token = encode_token(remember)

        delete_item(contact_type, contact_value, code)

        send_message(contact_type, contact_value, "Brief Box successfully authenticated.")

        return response(200, {"access_token": token}, event.raw_event)

    except Exception as e:
        logger.error(e)
        return response(500, {"message": f"{type(e).__name__}: {e}"}, event.raw_event)
