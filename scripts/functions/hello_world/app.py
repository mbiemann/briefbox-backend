from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

from common import response


logger = Logger()


@logger.inject_lambda_context(log_event=True)
@event_source(data_class=APIGatewayProxyEventV2)
def handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> dict:
    try:
        return response(200, {"message": "Hello, world!"}, event.raw_event)

    except Exception as e:
        logger.error(e)
        return response(500, {"message": f"{type(e).__name__}: {e}"}, event.raw_event)
