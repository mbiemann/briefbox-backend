from typing import TYPE_CHECKING

from aws_cdk.aws_lambda import Architecture, LayerVersion

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack


class PowertoolsLayer(LayerVersion):
    def __new__(cls, stack: "BriefBoxStack"):
        arch = "-Arm64" if const.PYTHON_ARCHITECTURE == Architecture.ARM_64 else ""
        return LayerVersion.from_layer_version_arn(
            scope=stack,
            id="powertools-layer",
            layer_version_arn=stack.format_arn(
                service="lambda",
                account="017000801446",
                resource=f"layer:AWSLambdaPowertoolsPythonV2{arch}:20",
            ),
        )
