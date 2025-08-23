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
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=[
                    "http://localhost:5173",
                    "https://michaelsvajhart.com", 
                    "https://www.michaelsvajhart.com"
                ],
                allow_methods=["GET", "POST"],
                allow_headers=apigateway.Cors.DEFAULT_HEADERS,
            )
        )
        
        # /sort route with Lambda integration
        sorting = self.api.root.add_resource("sort")

        sorting.add_method(
            "POST",
            apigateway.LambdaIntegration(
                _lambda.Function(
                    self, "SortLambdaHandler",
                    runtime=_lambda.Runtime.PYTHON_3_13,
                    handler="sorting.handler",
                    code=_lambda.Code.from_asset("lambda"),
                ),
                request_templates={"application/json": '{ "statusCode": "200" }'}
            )
        )