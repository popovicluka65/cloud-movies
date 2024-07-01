from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam, BundlingOptions, Duration,
    # aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_s3 as s3, aws_lambda_event_sources, RemovalPolicy,
    aws_cognito as cognito,
    aws_sns as sns
)
#import aws_cdk as core
from constructs import Construct

class CloudBackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "ContentBucket-New",
            bucket_name="content-bucket-cloud-app-movie2",

            cors=[
                s3.CorsRule(
                    allowed_methods=[
                        s3.HttpMethods.GET,
                        s3.HttpMethods.PUT,
                        s3.HttpMethods.POST,
                        s3.HttpMethods.DELETE,
                        s3.HttpMethods.HEAD
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"]
                )
            ],
            removal_policy=RemovalPolicy.DESTROY
        )

        s3_role = iam.Role(
            self, "S3AccessRole",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com")  # Postavljamo uslugu koja može koristiti ovu ulogu
        )

        # Dodavanje politike za dozvolu za pristup S3 bucketu
        s3_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                ],
                resources=[
                    "arn:aws:s3:::content-bucket-cloud-app-movie2/*"

                ]
            )
        )
        #
        # bucket_policy_statement = iam.PolicyStatement(
        #     effect=iam.Effect.ALLOW,
        #     actions=[
        #         "s3:GetObject",
        #         "s3:PutObject",
        #         "s3:DeleteObject"
        #     ],
        #     resources=[bucket.bucket_arn + "/*"],
        #     principals=[iam.AnyPrincipal()]
        # )
        #
        #
        # # Dodajemo politiku na S3 kantu
        # bucket.add_to_resource_policy(bucket_policy_statement)


        table = dynamodb.Table(
            self, 'MoviesTable',
            table_name='MoviesTable',
            partition_key={'name': 'movie_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'title', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_subscricions = dynamodb.Table(
            self, 'Subscription10Table',
            table_name='Subscription10Table',
            partition_key={'name': 'subscription_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'subscriber', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_review = dynamodb.Table(
            self, 'Review10Table',
            table_name='Review10Table',
            partition_key={'name': 'review_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_download = dynamodb.Table(
            self, 'Download10Table',
            table_name='Download10Table',
            partition_key={'name': 'download_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_interaction = dynamodb.Table(
            self, 'Interaction10Table',
            table_name='Interaction10Table',
            partition_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_feed = dynamodb.Table(
            self, 'Feed10Table',
            table_name='Feed10Table',
            partition_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        user_pool = cognito.UserPool(
            self, "MovieUserPoolNew",
            user_pool_name="MovieUserPoolNew",
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=False

            ),
            sign_in_aliases=cognito.SignInAliases(email=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True)
            )
        )

        client = cognito.UserPoolClient(
            self, "MovieUserPoolClientNew",
            user_pool=user_pool,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True
            ),
            generate_secret=False,
            o_auth={
                'flows': {
                    'implicit_code_grant': True,
                    'authorization_code_grant': True
                },
                'callback_urls': [
                    'http://localhost:4200/'
                ],
                'logout_urls': [
                    'http://localhost:4200/'
                ]
            },
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO
            ]
        )

        # Kreiranje SNS teme
        topic = sns.Topic(self, "MovieTopic",
                          display_name="MovieTopic",
                          topic_name="MovieTopic")

        actions_sns = [
             "sns:Publish"
        ]

        topic.add_to_resource_policy(
             statement=iam.PolicyStatement(
                 effect=iam.Effect.ALLOW,
                 actions=actions_sns,
                 principals=[iam.ServicePrincipal("lambda.amazonaws.com")],
                 resources=[topic.topic_arn]
             )
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
                    "dynamodb:DeleteItem",
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:PutObjectACL",
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminInitiateAuth",
                    "cognito-idp:AdminRespondToAuthChallenge",
                    "sns:Publish"
                ],
                resources=[
                    table.table_arn,
                    f"{bucket.bucket_arn}/*",
                    user_pool.user_pool_arn,
                    topic.topic_arn,
                    table_subscricions.table_arn,
                    table_review.table_arn,
                    table_download.table_arn,
                    table_interaction.table_arn,
                    table_feed.table_arn
                ]
            )
        )
        def create_lambda_function(id,name, handler, include_dir, method, layers, database_dynamo,database_s3):
            env='TABLE_NAME'
            if database_dynamo is not None:
                database=database_dynamo
            else:
                if database_dynamo is None and database_s3 is None:
                    database=""
                else:
                    env='BUCKET_NAME'
                    database=database_s3
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
                    env: database,
                    'USER_POOL_ID': user_pool.user_pool_id,
                    'TOPIC_ARN': topic.topic_arn
                },
                role=lambda_role
            )

            return function

        def upload_lambda_function(id, name, handler, include_dir, method, layers, database_dynamo, database_s3):

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
                    "TABLE_NAME": database_dynamo,
                    "BUCKET_NAME": database_s3
                },
                role=lambda_role
            )

            return function


        get_movie_lambda = create_lambda_function(
            "getMovies",
            "getMoviesFuction",
            "getMovies.lambda_handler",
            "getMovies",
            "GET",
            [],
            table.table_name,
            None
        )

        download_movie_lambda = upload_lambda_function(
            "getS3Content",
            "downloadContentS3",
            "downloadMovie.download_movie_handler",
            "downloadMovie",
            "GET",
            [],
            table.table_name,
            bucket.bucket_name
        )



        download_movie_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                ],
                resources=[
                    f"arn:aws:s3:::content-bucket-cloud-app-movie2/*",  # Dozvole za sve objekte unutar bucketa
                ]))

        subscribe_lambda = create_lambda_function(
            "postSubscribe",
            "subscribe",
            "subscribe.lambda_handler",
            "subscribe",
            "POST",
            [],
            table_subscricions.table_name,
            None
        )

        # Dodajte dozvole za pristup DynamoDB tabeli
        subscribe_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                ],
                resources=[
                    table_subscricions.table_arn
                ]
            )
        )

        get_feed_lambda = create_lambda_function(
            "getFeed",
            "getFeed",
            "getFeedHandler.get_feed_handler",
            "getFeed",
            "GET",
            [],
            table_feed.table_name,
            None
        )

        # Dodajte dozvole za pristup DynamoDB tabeli
        get_feed_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                ],
                resources=[
                    table_feed.table_arn
                ]
            )
        )

        put_interaction_lambda = create_lambda_function(
            "editInteraction",
            "editInteraction",
            "editInteractionHandler.lambda_handler",
            "editInteraction",
            "PUT",
            [],
            table_interaction.table_name,
            None
        )

        # Dodajte dozvole za pristup DynamoDB tabeli
        put_interaction_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                ],
                resources=[
                    table_interaction.table_arn
                ]
            )
        )
        # UPLOAD S3 AND DYNAMO DB---------------------------------------------------

        # upload_data_s3 = create_lambda_function(
        #     "uploadMovieToS3Bucket",
        #     "uploadMoviesFunctionS3",
        #     "uploadS3handler.upload_S3_handler",
        #     "s3Upload",
        #     "POST",
        #     [],
        #     None,
        #     bucket.bucket_name
        # )
        #
        # upload_data_s3.add_to_role_policy(
        #     iam.PolicyStatement(
        #         actions=[
        #             "s3:GetObject",
        #             "s3:PutObject",
        #         ],
        #         resources=[
        #             f"arn:aws:s3:::content-bucket-cloud-app-movie2/*",
        #         ]))
        #
        # upload_data_dynamo = create_lambda_function(
        #     "uploadMovieToDynamo",
        #     "uploadMoviesFunctionDynamo",
        #     "uploadDynamoHandler.upload_dynamo_handler",
        #     "dynamoUpload",
        #     "POST",
        #     [],
        #     table.table_name,
        #     None
        # )
        #
        # upload_data_s3_task = tasks.LambdaInvoke(
        #     self, 'InvokeLambdaS3',
        #     lambda_function=upload_data_s3,
        #     output_path='$.Payload'
        # )
        #
        # upload_data_dynamo_task = tasks.LambdaInvoke(
        #     self, 'InvokeLambdaDynamo',
        #     lambda_function=upload_data_dynamo,
        #     output_path='$.Payload'
        # )
        #
        # # Povezivanje zadataka u lanac
        # definition_body = upload_data_s3_task.next(upload_data_dynamo_task)
        #
        # # Kreiranje state machine
        # state_machine = sfn.StateMachine(
        #     self, 'MyStateMachine',
        #     definition_body=sfn.DefinitionBody.from_chainable(definition_body),
        #     timeout=Duration.minutes(10),  # Promenjen timeout
        #     # environment={
        #     #     'USER_POOL_ID': 'eu-central-1_rzNdae5DO'  # Replace with your user pool ID
        #     # }
        # )
        #
        # upload_data_s3.grant_invoke(state_machine.role)
        # upload_data_dynamo.grant_invoke(state_machine.role)
        # start_upload_data = create_lambda_function(
        #     "startUploadStep",
        #     "startUploadStepFunction",
        #     "startUploadMoviesHandler.upload_data_handler",
        #     "startUploadMovies",
        #     None,
        #     [],
        #     None,
        #     None
        # )
        #

        # Lambda funkcije
        first_lambda = lambda_.Function(
            self, "FirstLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="uploadS3handler.upload_S3_handler",
            code=lambda_.Code.from_asset("s3Upload")
        )

        second_lambda = lambda_.Function(
            self, "SecondLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="uploadDynamoHandler.upload_dynamo_handler",
            code=lambda_.Code.from_asset("dynamoUpload")
        )

        start_upload_data = lambda_.Function(
            self, "StartUploadData",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="startUploadMoviesHandler.upload_data_handler",
            code=lambda_.Code.from_asset("startUploadMovies")
        )

        # Definisanje Step Function-a
        first_task = tasks.LambdaInvoke(
            self, "First Task",
            lambda_function=first_lambda
        )

        second_task = tasks.LambdaInvoke(
            self, "Second Task",
            lambda_function=second_lambda
        )

        definition = first_task.next(second_task)

        state_machine = sfn.StateMachine(
            self, "StateMachine",
            definition=definition
        )

        # Dodela dozvole Lambda funkciji da pokrene Step Function
        state_machine.grant_start_execution(start_upload_data)
        start_upload_data.add_environment('STATE_MACHINE_ARN', state_machine.state_machine_arn)

        # state_machine.grant_start_execution(start_upload_data)

        # Optionally, add permissions to the Step Function execution role



        api_gateway_role = iam.Role(self, "ApiGatewayRole",
                                    assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
                                    description="Role for API Gateway to invoke lambda functions")


        # Dodaj potrebne permisije roli
        api_gateway_role.add_to_policy(iam.PolicyStatement(
            actions=["lambda:InvokeFunction"],
            resources=["*"]  # mogu ovde stativi specificirane lambde
        ))

        #bucket.grant_read_write(start_upload_data)

        # Dodavanje dozvola Lambda funkciji za pristup DynamoDB tabeli
        table.grant_read_data(get_movie_lambda)
        table_subscricions.add_global_secondary_index(
            index_name='subscriber-index',
            partition_key={'name': 'subscriber', 'type': dynamodb.AttributeType.STRING}
        )
        table_subscricions.grant_read_write_data(subscribe_lambda)

        table_subscricions.grant_read_write_data(put_interaction_lambda)


        bucket.grant_read_write(download_movie_lambda)
        bucket.grant_read_write(subscribe_lambda)
        bucket.grant_read_write(put_interaction_lambda)
        bucket.grant_read_write(get_feed_lambda)

        self.api = apigateway.RestApi(self, "CloudProjectTeam14",
                                 rest_api_name="CloudProject2023",
                                 description="This service serves movie contents.",
                                 endpoint_types=[apigateway.EndpointType.REGIONAL],
                                 default_cors_preflight_options={
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS
                                 },

                               )

        get_movie_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        download_movie_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )


        start_upload_data.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        subscribe_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        get_feed_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        put_interaction_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        movie_resource = self.api.root.add_resource("movieNew")

        # GET metoda za /movies123
        get_movies_integration = apigateway.LambdaIntegration(get_movie_lambda, credentials_role=api_gateway_role, proxy=True)
        self.api.root.add_resource("movies123").add_method("GET", get_movies_integration)

        # POST metoda za /movie
        movie_resource = self.api.root.add_resource("movie")
        movie_resource.add_method("POST", apigateway.LambdaIntegration(start_upload_data, credentials_role=api_gateway_role, proxy=True))

        # POST metoda za /movieS3
        self.api.root.add_resource("movieS3").add_method("POST", apigateway.LambdaIntegration(start_upload_data, credentials_role=api_gateway_role, proxy=True))

        # GET metoda za /movie/{movieId}
        movie_resource_with_id = movie_resource.add_resource("{movieName}")
        movie_resource_with_id.add_method("GET", apigateway.LambdaIntegration(download_movie_lambda,
                                                                              credentials_role=api_gateway_role,
                                                                              proxy=True))

        # GET metoda za /downloadS3Content/{contentId}
        download_s3_resource_with_id = self.api.root.add_resource("downloadS3Content")
        download_s3_resource_with_id_with_id = download_s3_resource_with_id.add_resource("{contentName}")
        download_s3_resource_with_id_with_id.add_method("GET", apigateway.LambdaIntegration(download_movie_lambda,
                                                                                            credentials_role=api_gateway_role,
                                                                                            proxy=True))
        subsribe_resource = self.api.root.add_resource("subscribe")
        subsribe_resource.add_method("POST",
                                  apigateway.LambdaIntegration(subscribe_lambda, credentials_role=api_gateway_role,
                                                               proxy=True))

        interaction_resource = self.api.root.add_resource("interaction")
        interaction_resource.add_method("PUT",
                                     apigateway.LambdaIntegration(put_interaction_lambda, credentials_role=api_gateway_role,
                                                                  proxy=True))

        new_rute = self.api.root.add_resource("getFromS3")
        new_rute_id = new_rute.add_resource("{id}")
        new_rute_id.add_method("GET", apigateway.LambdaIntegration(download_movie_lambda, proxy=True))

        # deployment nakon dodavanja svih resursa i metoda
        api_deployment_new = apigateway.Deployment(self, "ApiDeploymentTotalNew",
                                                   api=self.api)

        # novi stage
        apigateway.Stage(self, "NewStage",
                         deployment=api_deployment_new,
                         stage_name="noviStage")