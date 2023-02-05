from aws_lambda_powertools.utilities.parameters import get_parameter
from behave import when
from requests import get, post


@when(u'I send code')
def step_impl(context):

    # # Auth Code by SMS
    # resp = post(
    #     url=f"{context.api_url}/auth/code",
    #     json={
    #         "sms": get_parameter("/briefbox/inputs/briefbox/behave-sms"),
    #     },
    # )
    # assert resp.status_code == 200

    # # Auth Code by Email
    # resp = post(
    #     url=f"{context.api_url}/auth/code",
    #     json={
    #         "email": get_parameter("/briefbox/inputs/briefbox/behave-email"),
    #     },
    # )
    # assert resp.status_code == 200

    print()


@when(u'I token')
def step_impl(context):

    # # Auth Token by SMS
    # resp = post(
    #     url=f"{context.api_url}/auth/token",
    #     json={
    #         "sms": get_parameter("/briefbox/inputs/briefbox/behave-sms"),
    #         "code": "",
    #     },
    # )
    # assert resp.status_code == 200
    # token = resp.json()["access_token"]

    # # Auth Token by Email
    # resp = post(
    #     url=f"{context.api_url}/auth/token",
    #     json={
    #         "email": get_parameter("/briefbox/inputs/briefbox/behave-email"),
    #         "code": "",
    #         "remember": "Y",
    #     },
    # )
    # print()
    # print(f"{resp.status_code} {resp.text}")
    # print()
    # assert resp.status_code == 200
    # token = resp.json()["access_token"]

    # # Hello World
    # resp = get(
    #     url=f"{context.api_url}/helloworld",
    #     headers={
    #         "Authorization": token,
    #     },
    # )
    # print()
    # print(f"{resp.status_code} {resp.text}")
    # print()
    # assert resp.status_code == 200
    # assert resp.json()["message"] == "Hello, world!"

    print()
