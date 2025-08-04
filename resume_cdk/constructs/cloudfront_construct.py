from constructs import Construct
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as certificatemanger,
    aws_iam as iam,
    RemovalPolicy,
    Duration
)

class CloudfrontConstruct(Construct):
    def __init__(self, scope: Construct, id: str, account: str,  **kwargs):
        super().__init__(scope, id, **kwargs)

        self.bucket = s3.Bucket(self, f"{id}-bucket",
            bucket_name=f"{id.lower()}-bucket",
            website_index_document="index.html",
            website_error_document="error.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL, # Recommended for security
            removal_policy=RemovalPolicy.DESTROY, # For easy cleanup during development
            auto_delete_objects=True # For easy cleanup during development
        )
        
        self.distribution = cloudfront.Distribution(self, f"{id}-distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(self.bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            domain_names=["michaelsvajhart.com", "www.michaelsvajhart.com"],
            certificate=certificatemanger.Certificate.from_certificate_arn(self, "SiteCertificate", "arn:aws:acm:us-east-1:250421909163:certificate/388e5f30-ed64-4315-b0ed-027c2ded5993"),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=404,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30)
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=404,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(30)
                )
            ],
            price_class=cloudfront.PriceClass.PRICE_CLASS_100
        )

        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                sid="AllowCloudFrontServicePrincipalReadOnly",
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                actions=["s3:GetObject"],
                resources=[self.bucket.arn_for_objects("*")],
                conditions={
                    "ArnLike": {
                        "aws:SourceArn": f"arn:aws:cloudfront::{account}:distribution/{self.distribution.distribution_id}"
                    }
                }
            )
        )