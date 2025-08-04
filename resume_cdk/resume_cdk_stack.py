from aws_cdk import (
    Stack,
)
from constructs import Construct
from .constructs.cloudfront_construct import CloudfrontConstruct
from .constructs.api_gateway_construct import ApiGatewayConstruct


class ResumeCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stack_name = self.stack_name

        
        fe = CloudfrontConstruct(self, f"{stack_name}-cloudfront", self.account)
        
        api = ApiGatewayConstruct(self, f"{stack_name}-apigateway")

        
        