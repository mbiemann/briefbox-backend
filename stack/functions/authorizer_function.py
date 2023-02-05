from typing import TYPE_CHECKING

from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_ssm import StringParameter

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack
    from stack.layers.auth_layer import AuthLayer
    from stack.layers.common_layer import CommonLayer
    from stack.layers.powertools_layer import PowertoolsLayer


class AuthorizerFunction(PythonFunction):
    def __init__(self, stack: "BriefBoxStack", secret_token_param: StringParameter, auth_layer: "AuthLayer", common_layer: "CommonLayer", powertools_layer: "PowertoolsLayer"):
        super().__init__(
            scope=stack,
            id="authorizer",
            function_name=f"{stack.stack_name}-authorizer",
            entry="./scripts/functions/authorizer",
            index="app.py",
            handler="handler",
            architecture=const.PYTHON_ARCHITECTURE,
            runtime=const.PYTHON_RUNTIME,
            timeout=const.LAMBDA_TIMEOUT,
            layers=[
                auth_layer,
                common_layer,
                powertools_layer,
            ],
            environment={
                "SECRET_TOKEN_PARAM_NAME": secret_token_param.parameter_name,
                "POWERTOOLS_SERVICE_NAME": f"{stack.stack_name}-authorizer",
                "LOG_LEVEL": const.LOG_LEVEL,
            },
        )
        self._permissions(secret_token_param)


    def _permissions(self, secret_token_param: StringParameter):
        secret_token_param.grant_read(self)
