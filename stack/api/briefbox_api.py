from typing import TYPE_CHECKING

from aws_cdk import Duration
from aws_cdk.aws_apigatewayv2_alpha import HttpApi, HttpMethod, CorsPreflightOptions, CorsHttpMethod
from aws_cdk.aws_apigatewayv2_authorizers_alpha import HttpLambdaAuthorizer, HttpLambdaResponseType
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack
    from stack.functions.auth_code_function import AuthCodeFunction
    from stack.functions.auth_token_function import AuthTokenFunction
    from stack.functions.authorizer_function import AuthorizerFunction
    from stack.functions.hello_world_function import HelloWorldFunction


class BriefBoxAPI(HttpApi):
    _api_authorizer: HttpLambdaAuthorizer
    stage_url: str

    def __init__(self, stack: "BriefBoxStack", auth_code_func: "AuthCodeFunction", auth_token_func: "AuthTokenFunction", authorizer_func: "AuthorizerFunction", hello_world_func: "HelloWorldFunction"):
        super().__init__(
            scope=stack,
            id="api",
            api_name=f"{stack.stack_name}-api",
            create_default_stage=False,
            cors_preflight=CorsPreflightOptions(
                allow_origins=["*"],
                allow_headers=["*"],
                allow_methods=[CorsHttpMethod.ANY],
            ),
        )
        self._stage()
        self._authorizer(authorizer_func)
        self._routes(auth_code_func, auth_token_func, hello_world_func)


    def _stage(self):
        stage = self.add_stage(
            id="api-stage",
            stage_name=const.API_STAGE_NAME,
            auto_deploy=True,
        )
        self.stage_url = stage.url


    def _authorizer(self, authorizer_func: "AuthorizerFunction"):
        self._api_authorizer = HttpLambdaAuthorizer(
            id="api-authorizer",
            handler=authorizer_func,
            response_types=[HttpLambdaResponseType.SIMPLE],
            results_cache_ttl=Duration.seconds(1440),
        )


    def _routes(self, auth_code_func: "AuthCodeFunction", auth_token_func: "AuthTokenFunction", hello_world_func: "HelloWorldFunction"):

        # (PUBLIC) POST /auth/code
        self._add_route(
            path="/auth/code",
            method=HttpMethod.POST,
            handler=auth_code_func,
            public=True,
        )

        # (PUBLIC) POST /auth/token
        self._add_route(
            path="/auth/token",
            method=HttpMethod.POST,
            handler=auth_token_func,
            public=True,
        )

        # GET /helloworld
        self._add_route(
            path="/helloworld",
            method=HttpMethod.GET,
            handler=hello_world_func,
        )


    def _add_route(self, path, method, handler, *, public = False):
        self.add_routes(
            path=path,
            methods=[method],
            authorizer=None if public else self._api_authorizer,
            integration=HttpLambdaIntegration(
                id=f"{path}-{method}",
                handler=handler,
            ),
        )
