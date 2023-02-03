from json import loads


def test_handler(module):
    assert loads(module.handler({}, None)["body"]) == {"message": "Hello, auth challenge world!", "event": {}}
