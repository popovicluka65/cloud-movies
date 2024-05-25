from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam, BundlingOptions, Duration,
    # aws_sqs as sqs,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class CloudBackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CloudBackQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "CdkPythonStarterTopic"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))

        # Kreiranje DynamoDB tabelu
        # movie_table = dynamodb.Table(
        #     self, "movie_table",
        #     table_name="movie_table",
        #     partition_key=dynamodb.Attribute(
        #         name="id",
        #         type=dynamodb.AttributeType.STRING
        #     ),
        #     removal_policy=dynamodb.RemovalPolicy.RETAIN,
        # )
        #GATEWAY
        #LAMBDE + DYNAMODB I S3


        # self.api.root.add_method("ANY")

        # my_lambda = _lambda.Function(
        #     self, 'MyLambda',
        #     runtime=_lambda.Runtime.PYTHON_3_8,
        #     handler='lambda_handler.handler',
        #     code=_lambda.Code.from_asset('lambda')  # Pretpostavlja se da imate 'lambda' folder sa kodom
        # )

        #table.grant_read_write_data(post_lambda)

        #
        # # Povezivanje Lambda funkcije sa API Gateway-om
        # items = self.api.root.add_resource("items")
        # items.add_method("GET", apigateway.LambdaIntegration(my_lambda))

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
            fn_url = function.add_function_url(
                auth_type=_lambda.FunctionUrlAuthType.NONE,
                cors=_lambda.FunctionUrlCorsOptions(
                    allowed_origins=["*"]
                )
            )

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
        self.api = apigateway.RestApi(
            self, 'Api',
            rest_api_name='MovieCloudProject',
            description='This is api gateway for movies.'
        )


        # Dodavanje dozvola Lambda funkciji za pristup DynamoDB tabeli
        table.grant_read_data(get_movie_lambda)

        get_movies_integration = apigateway.LambdaIntegration(get_movie_lambda)

        self.api.root.add_resource("movies").add_method("GET", get_movies_integration)