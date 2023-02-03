from behave import when
from requests import post


@when(u'I run this scenario')
def step_impl(context):

    # Auth Code
    resp = post(
        url=f"{context.api_url}/auth/code",
    )
    print(f"{resp.status_code} {resp.text}")
    assert resp.status_code == 200

    # Auth Challenge
    resp = post(
        url=f"{context.api_url}/auth/challenge",
    )
    print(f"{resp.status_code} {resp.text}")
    assert resp.status_code == 200
