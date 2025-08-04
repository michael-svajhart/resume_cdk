from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
)

class ApiGatewayConstruct(Construct):
    def __init__(self, scope: Construct, id: str,  **kwargs):
        super().__init__(scope, id, **kwargs)

        self.api = apigateway.RestApi(
            self, f"{id}-RestApi",
            rest_api_name=f"{id}-RestApi",
            description="This is my sample API built with CDK.",
        )
        
         # /hello route
        hello = self.api.root.add_resource("hello")

         # Lambda function
        hello_lambda = _lambda.Function(
            self, "HelloLambdaHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        # Lambda integration
        lambda_integration = apigateway.LambdaIntegration(
            hello_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        hello.add_method("GET", lambda_integration)

         # /test route
        test = self.api.root.add_resource("test")

         # Lambda function
        test_lambda = _lambda.Function(
            self, "TestingoLambdaHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="testing.handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        # Lambda integration
        test_integration = apigateway.LambdaIntegration(
            test_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        test.add_method("GET", test_integration)