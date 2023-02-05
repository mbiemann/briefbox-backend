from json import dumps
from os import getenv

from aws_lambda_powertools import Logger


logger = Logger()


class EnvironmentVariableNotFound(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Environment Variable {name} not found.")


def get_required_var(name):
    logger.debug(f"Getting required value of environment variable {name}.")
    value = getenv(name)
    
    if not value:
        logger.exception(f"Not found value from environment variable {name}.")
        raise EnvironmentVariableNotFound(name)
    
    logger.debug(f"Got value {value} of environment variable {name}.")
    return value


def response(status_code: int, body: dict, request: dict = None):

    headers = {"Content-Type": "application/json"}

    if request and logger.log_level == "DEBUG":
        headers["Request"] = dumps(request)

    response = {
        "statusCode": status_code,
        "headers": headers,
        "body": dumps(body),
    }

    logger.debug(f"Response: {response}")

    return response
