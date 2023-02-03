from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_ssm import StringParameter

import stack.constants as const


class AuthCodeFunction(PythonFunction):
    def __init__(self, stack):
        super().__init__(
            scope=stack,
            id="auth-code",
            function_name=f"{stack.stack_name}-auth-code",
            entry="./scripts/functions/auth_code",
            index="app.py",
            handler="handler",
            architecture=const.PYTHON_ARCHITECTURE,
            runtime=const.PYTHON_RUNTIME,
            environment={
                "POWERTOOLS_SERVICE_NAME": stack.stack_name,
                "LOG_LEVEL": "INFO",
            },
        )
