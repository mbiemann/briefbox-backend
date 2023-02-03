from typing import TYPE_CHECKING

from aws_cdk.aws_apigatewayv2_alpha import HttpApi, HttpMethod
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack
    from stack.functions.auth_code_function import AuthCodeFunction
    from stack.functions.auth_challenge_function import AuthChallengeFunction


class BriefBoxAPI(HttpApi):
    stage_url: str

    def __init__(self, stack: "BriefBoxStack", auth_code_func: "AuthCodeFunction", auth_challenge_func: "AuthChallengeFunction"):
        super().__init__(
            scope=stack,
            id="api",
            api_name=f"{stack.stack_name}-api",
            create_default_stage=False,
        )
        stage = self.add_stage(
            id="api-stage",
            stage_name=const.API_STAGE_NAME,
            auto_deploy=True,
        )
        self.stage_url = stage.url
        
        # (PUBLIC) POST /auth/code
        self._add_route(
            path="/auth/code",
            method=HttpMethod.POST,
            handler=auth_code_func,
        )

        # (PUBLIC) POST /auth/challenge
        self._add_route(
            path="/auth/challenge",
            method=HttpMethod.POST,
            handler=auth_challenge_func,
        )


    def _add_route(self, path, method, handler):
        self.add_routes(
            path=path,
            methods=[method],
            authorizer=None,
            integration=HttpLambdaIntegration(
                id=f"{path}-{method}",
                handler=handler,
            ),
        )
