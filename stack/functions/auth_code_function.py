from typing import TYPE_CHECKING

from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_ssm import StringParameter

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack
    from stack.layers.auth_layer import AuthLayer
    from stack.layers.common_layer import CommonLayer
    from stack.layers.powertools_layer import PowertoolsLayer
    from stack.tables.auth_table import AuthTable


class AuthCodeFunction(PythonFunction):
    def __init__(self, stack: "BriefBoxStack", source_email_param: StringParameter, auth_table: "AuthTable", auth_layer: "AuthLayer", common_layer: "CommonLayer", powertools_layer: "PowertoolsLayer"):
        super().__init__(
            scope=stack,
            id="auth-code",
            function_name=f"{stack.stack_name}-auth-code",
            entry="./scripts/functions/auth_code",
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
                "AUTH_TABLE_NAME": auth_table.table_name,
                "SOURCE_EMAIL": source_email_param.string_value,
                "POWERTOOLS_SERVICE_NAME": f"{stack.stack_name}-auth-code",
                "LOG_LEVEL": const.LOG_LEVEL,
            },
        )
        self._permissions(auth_table)
    

    def _permissions(self, auth_table: "AuthTable"):
        auth_table.grant_write_data(self)

        self.add_to_role_policy(PolicyStatement(
            actions=[
                "ses:SendEmail",
                "sns:Publish",
            ],
            resources=["*"],
        ))
