from aws_cdk import App, Stack

from stack.functions.auth_code_function import AuthCodeFunction


class BriefBoxStack(Stack):

    def __init__(self, app: App):
        super().__init__(
            scope=app,
            id="briefbox",
        )

        AuthCodeFunction(self)
