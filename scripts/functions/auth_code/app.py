from random import randint

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

from auth import contact_from_body, put_item, send_message
from common import response


logger = Logger()


@logger.inject_lambda_context(log_event=True)
@event_source(data_class=APIGatewayProxyEventV2)
def handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> dict:
    try:
        contact_type, contact_value = contact_from_body(event.json_body)
        code = str(randint(100000, 999999))

        put_item(contact_type, contact_value, code)

        send_message(contact_type, contact_value, f"Brief Box authentication code: {code}.")
        
        return response(200, {"message": "Code successfully sent."}, event.raw_event)

    except Exception as e:
        logger.error(e)
        return response(500, {"message": f"{type(e).__name__}: {e}"}, event.raw_event)
