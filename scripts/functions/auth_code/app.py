from json import dumps


def _response(status_code: int, body: dict = None, *, error: Exception = None) -> dict:
    if error:
        if not body:
            body = {}
        body["error"] = f"{type(error).__name__}: {error}"
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": dumps(body),
    }


def handler(event, _) -> dict:
    try:
        return _response(200, {"message": "Hello, world!", "event": event})

    except Exception as e:
        return _response(500, {"event": event}, error=e)
