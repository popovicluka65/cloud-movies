from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam, BundlingOptions, Duration,
    # aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_s3 as s3
)
from constructs import Construct

class CloudBackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # S3 bucket
        # bucket = s3.Bucket(self, "MovieBucket", versioned=True)

        table = dynamodb.Table(
            self, 'MoviesTable',
            table_name='MoviesTable',
            partition_key={'name': 'movie_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'title', 'type': dynamodb.AttributeType.STRING},
        )

        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem"
                ],
                resources=[table.table_arn]
            )
        )

        def create_lambda_function(id,name, handler, include_dir, method, layers):
            function = _lambda.Function(
                self, id,
                function_name=name,
                runtime=_lambda.Runtime.PYTHON_3_9,
                layers=layers,
                handler=handler,
                code=_lambda.Code.from_asset(include_dir,
                                             # bundling=BundlingOptions(
                                             #     image=_lambda.Runtime.PYTHON_3_9.bundling_image,
                                             #     command=[
                                             #          "cmd.exe", "/c",  # Koristimo cmd.exe za pokretanje komandi na Windows-u
                                             # "pip install --no-cache -r requirements.txt -t . && copy .\\* ..\\asset-output"
                                             #     ],
                                             # ),
                                             ),
                memory_size=128,
                timeout=Duration.seconds(10),
                environment={
                    'TABLE_NAME': table.table_name
                },
                role=lambda_role
            )
            # fn_url = function.add_function_url(
            #     auth_type=_lambda.FunctionUrlAuthType.NONE,
            #     cors=_lambda.FunctionUrlCorsOptions(
            #         allowed_origins=["https://localhost:4200"],
            #         #allowed_methods=["GET", "POST", "OPTIONS"],
            #         allowed_headers=["Content-Type"],
            #         # max_age=core.Duration.seconds(300)  # Opcionalno: keširanje preflight odgovora
            #     )
            # )

            return function


        get_movie_lambda = create_lambda_function(
            "getMovies",
            "getMoviesFuction",
            "getMovies.lambda_handler",
            "getMovies",
            "GET",
            []
        )
        #
        # ----------------------------------------------

        # Lambda Function: Upload to S3
        # upload_to_s3_lambda = create_lambda_function(
        #     "postMovies", "updateMovieS3", "postMovies.s3_handler", "postMovies", "POST", []
        # )
        # upload_to_s3_lambda = _lambda.Function(
        #     self, "UploadToS3Lambda",
        #     runtime=_lambda.Runtime.PYTHON_3_8,
        #     handler="postMovies.s3_handler",
        #     code=_lambda.Code.asset("lambda"),
        #     environment={
        #         "BUCKET_NAME": bucket.bucket_name
        #     }
        # )
        # bucket.grant_put(upload_to_s3_lambda)
        #
        # # Lambda Function: Save metadata to DynamoDB
        # save_metadata_lambda = _lambda.Function(
        #     self, "SaveMetadataLambda",
        #     runtime=_lambda.Runtime.PYTHON_3_8,
        #     handler="save_metadata_to_dynamodb.lambda_handler",
        #     code=_lambda.Code.asset("lambda"),
        #     environment={
        #         "TABLE_NAME": table.table_name
        #     }
        # )
        # table.grant_write_data(save_metadata_lambda)
        #
        # # Step Function Tasks
        # upload_to_s3_task = tasks.LambdaInvoke(
        #     self, "UploadToS3",
        #     lambda_function=upload_to_s3_lambda,
        #     output_path="$.Payload"
        # )
        #
        # save_metadata_task = tasks.LambdaInvoke(
        #     self, "SaveMetadata",
        #     lambda_function=save_metadata_lambda,
        #     output_path="$.Payload"
        # )
        #
        # # Step Function Definition
        # definition = upload_to_s3_task.next(save_metadata_task)
        #
        # # Step Function
        # state_machine = sfn.StateMachine(
        #     self, "StateMachine",
        #     definition=definition
        # )


        # --------------




        # ------------

        # self.api = apigateway.RestApi(
        #     self, 'Api',
        #     rest_api_name='MovieCloudProject',
        #     description='This is api gateway for movies.'
        # )

        self.api = apigateway.RestApi(self, "MovieCloudApps",
                                 rest_api_name="Movie apps",
                                 description="This service serves movie contents.",
                                 endpoint_types=[apigateway.EndpointType.REGIONAL],
                                 default_cors_preflight_options={
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS
                                 }
                                 )


        # Dodavanje dozvola Lambda funkciji za pristup DynamoDB tabeli
        table.grant_read_data(get_movie_lambda)

        get_movies_integration = apigateway.LambdaIntegration(get_movie_lambda)

        self.api.root.add_resource("movies").add_method("GET", get_movies_integration)

