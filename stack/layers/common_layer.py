from typing import TYPE_CHECKING

from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion

import stack.constants as const

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack


class CommonLayer(PythonLayerVersion):
    def __init__(self, stack: "BriefBoxStack"):
        super().__init__(
            scope=stack,
            id="common-layer",
            layer_version_name=f"{stack.stack_name}-common",
            entry="./scripts/layers/common",
            compatible_architectures=[
                const.PYTHON_ARCHITECTURE,
            ],
            compatible_runtimes=[
                const.PYTHON_RUNTIME,
            ],
        )
