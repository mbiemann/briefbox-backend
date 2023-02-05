from typing import TYPE_CHECKING

from aws_cdk.aws_lambda_python_alpha import PythonFunction

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack
    from stack.layers.common_layer import CommonLayer
    from stack.layers.powertools_layer import PowertoolsLayer


class HelloWorldFunction(PythonFunction):
    def __init__(self, stack: "BriefBoxStack", common_layer: "CommonLayer", powertools_layer: "PowertoolsLayer"):
        super().__init__(
            scope=stack,
            id="hello-world",
            function_name=f"{stack.stack_name}-hello-world",
            entry="./scripts/functions/hello_world",
            index="app.py",
            handler="handler",
            architecture=const.PYTHON_ARCHITECTURE,
            runtime=const.PYTHON_RUNTIME,
            timeout=const.LAMBDA_TIMEOUT,
            layers=[
                common_layer,
                powertools_layer,
            ],
            environment={
                "POWERTOOLS_SERVICE_NAME": f"{stack.stack_name}-hello-world",
                "LOG_LEVEL": const.LOG_LEVEL,
            },
        )
