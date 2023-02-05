from aws_cdk import App, Stack
from aws_cdk.aws_ssm import StringParameter

from stack.api.briefbox_api import BriefBoxAPI
from stack.layers.auth_layer import AuthLayer
from stack.layers.common_layer import CommonLayer
from stack.layers.powertools_layer import PowertoolsLayer
from stack.functions.auth_code_function import AuthCodeFunction
from stack.functions.auth_token_function import AuthTokenFunction
from stack.functions.authorizer_function import AuthorizerFunction
from stack.functions.hello_world_function import HelloWorldFunction
from stack.tables.auth_table import AuthTable
import stack.constants as const


class BriefBoxStack(Stack):
    def __init__(self, app: App):
        super().__init__(
            scope=app,
            id="briefbox",
        )
        self._resources()

    
    def _resources(self):
        api_url_param_name = f"{const.PARAM_PREFIX_OUTPUT}/{self.stack_name}/api-url"

        # Input Parameters
        source_email_param = self._input_parameter("source-email")
        secret_token_param = self._input_parameter("secret-token", decrypt=True)

        # DynamoDB Tables
        auth_table = AuthTable(self)

        # Lambda Layers
        auth_layer = AuthLayer(self)
        common_layer = CommonLayer(self)
        powertools_layer = PowertoolsLayer(self)

        # Lambda Functions
        auth_code_func = AuthCodeFunction(self, source_email_param, auth_table, auth_layer, common_layer, powertools_layer)
        auth_token_func = AuthTokenFunction(self, source_email_param, secret_token_param, auth_table, auth_layer, common_layer, powertools_layer)
        authorizer_func = AuthorizerFunction(self, secret_token_param, auth_layer, common_layer, powertools_layer)
        hello_world_func = HelloWorldFunction(self, common_layer, powertools_layer)

        # API Gateway
        api = BriefBoxAPI(self, auth_code_func, auth_token_func, authorizer_func, hello_world_func)

        # Output Parameters
        StringParameter(
            scope=self,
            id="api-url",
            parameter_name=api_url_param_name,
            string_value=api.stage_url,
        )


    def _input_parameter(self, name: str, *, decrypt = False) -> StringParameter:
        if decrypt:
            return StringParameter.from_secure_string_parameter_attributes(
                scope=self,
                id=f"{name}-param",
                parameter_name=f"{const.PARAM_PREFIX_INPUT}/{self.stack_name}/{name}",
            )
        else:
            return StringParameter.from_string_parameter_name(
                scope=self,
                id=f"{name}-param",
                string_parameter_name=f"{const.PARAM_PREFIX_INPUT}/{self.stack_name}/{name}",
            )
