from aws_cdk.aws_lambda_python_alpha import PythonFunction

import stack.constants as const


class AuthChallengeFunction(PythonFunction):
    def __init__(self, stack):
        super().__init__(
            scope=stack,
            id="auth-challenge",
            function_name=f"{stack.stack_name}-auth-challenge",
            entry="./scripts/functions/auth_challenge",
            index="app.py",
            handler="handler",
            architecture=const.PYTHON_ARCHITECTURE,
            runtime=const.PYTHON_RUNTIME,
            environment={
                "POWERTOOLS_SERVICE_NAME": stack.stack_name,
                "LOG_LEVEL": "INFO",
            },
        )
