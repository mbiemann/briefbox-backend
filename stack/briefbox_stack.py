from aws_cdk import App, Stack

class BriefBoxStack(Stack):
    def __init__(self, app: App):
        super().__init__(
            scope=app,
            id="briefbox",
        )
