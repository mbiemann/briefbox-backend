from aws_cdk import App, Stack
from aws_cdk.aws_ssm import StringParameter

from stack.api.briefbox_api import BriefBoxAPI
from stack.functions.auth_code_function import AuthCodeFunction
from stack.functions.auth_challenge_function import AuthChallengeFunction
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

        # Lambda Functions
        auth_code_func = AuthCodeFunction(self)
        auth_challenge_func = AuthChallengeFunction(self)

        # API Gateway
        api = BriefBoxAPI(self, auth_code_func, auth_challenge_func)

        # Output Parameters
        StringParameter(
            scope=self,
            id="api-url",
            parameter_name=api_url_param_name,
            string_value=api.stage_url,
        )
