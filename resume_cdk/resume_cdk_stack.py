from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as certificatemanger,
    RemovalPolicy,
    Duration
)
from constructs import Construct

class ResumeCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stack_name = self.stack_name
 
        website_bucket = s3.Bucket(self, f"{stack_name}-fe-bucket",
            bucket_name=f"{stack_name.lower()}-fe-bucket",
            website_index_document="index.html",
            website_error_document="error.html",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL, # Recommended for security
            removal_policy=RemovalPolicy.DESTROY, # For easy cleanup during development
            auto_delete_objects=True # For easy cleanup during development
        )
        oac = cloudfront.S3OriginAccessControl(self, "MyOAC",
            signing=cloudfront.Signing.SIGV4_NO_OVERRIDE
        )
 
        s3_origin = origins.S3BucketOrigin.with_origin_access_control(website_bucket,
            origin_access_control=oac
        )
 
        # certificateArn="arn:aws:acm:us-east-1:607458310393:certificate/86b15f14-bf6d-4ad7-b010-33e4c597345e"
        # cert = certificatemanger.Certificate.fromCertificateArn(self, "SiteCertificate",
        #     certificateArn)
 
 
        distro = cloudfront.Distribution(self, "distro",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            # domain_names=[""]
            # certificate: cert,
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                   http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30)
                ),
                cloudfront.ErrorResponse(
                   http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30)
                )
            ],
            price_class=cloudfront.PriceClass.PRICE_CLASS_100
        )