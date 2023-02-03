from aws_cdk.aws_lambda import Architecture, Runtime

API_STAGE_NAME = "v1"
PYTHON_ARCHITECTURE = Architecture.X86_64
PYTHON_RUNTIME = Runtime.PYTHON_3_7

PARAM_PREFIX = "/briefbox"
PARAM_PREFIX_INPUT = f"{PARAM_PREFIX}/inputs"
PARAM_PREFIX_OUTPUT = f"{PARAM_PREFIX}/outputs"
