from typing import TYPE_CHECKING

from aws_cdk.aws_dynamodb import Attribute, AttributeType, Table

if TYPE_CHECKING:
    from stack.briefbox_stack import BriefBoxStack


class AuthTable(Table):
    def __init__(self, stack: "BriefBoxStack"):
        super().__init__(
            scope=stack,
            id="auth-table",
            table_name=f"{stack.stack_name}-auth-code",
            partition_key=Attribute(
                name="auth",
                type=AttributeType.STRING,
            ),
            time_to_live_attribute="ttl",
        )
