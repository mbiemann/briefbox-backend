from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerEventV2,
    APIGatewayAuthorizerResponseV2,
)

from auth import check_token


@event_source(data_class=APIGatewayAuthorizerEventV2)
def handler(event: APIGatewayAuthorizerEventV2, _):
    try:
        if check_token(event.get_header_value("authorization")):
            return APIGatewayAuthorizerResponseV2(authorize=True).asdict()
    except:
        pass
    raise Exception("Unauthorized")
