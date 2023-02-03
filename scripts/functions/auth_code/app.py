from json import dumps


def handler(event, _) -> dict:
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": dumps({
            "message": "Hello, auth code world!",
            "event": event,
        }),
    }
