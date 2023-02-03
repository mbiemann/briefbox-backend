from boto3 import client


def before_all(context):
    context.api_url = client("ssm").get_parameter(Name=f"/briefbox/outputs/briefbox/api-url")["Parameter"]["Value"]
