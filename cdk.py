import aws_cdk as cdk
from stack.briefbox_stack import BriefBoxStack
app = cdk.App()
BriefBoxStack(app)
app.synth()
