from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam, BundlingOptions, Duration,
    # aws_sqs as sqs,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_s3 as s3, aws_lambda_event_sources, RemovalPolicy,
    aws_cognito as cognito,
    aws_sns as sns,
    custom_resources as cr,
    aws_sqs as sqs,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_lambda_event_sources as lambda_event_sources,
    aws_dynamodb as dynamodb,

)
from aws_cdk.aws_lambda import LayerVersion
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_s3_notifications as s3n
# import aws_cdk as core
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
            self, 'MoviesTable100',
            table_name='MoviesTable100',
            partition_key={'name': 'movie_id', 'type': dynamodb.AttributeType.STRING},
            # sort_key={'name': 'title', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_subscricions = dynamodb.Table(
            self, 'Subscription100Table',
            table_name='Subscription100Table',
            partition_key={'name': 'subscription_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'subscriber', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_review = dynamodb.Table(
            self, 'Review100Table',
            table_name='Review100Table',
            partition_key={'name': 'review_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_download = dynamodb.Table(
            self, 'Download100Table',
            table_name='Download100Table',
            partition_key={'name': 'download_id', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_interaction = dynamodb.Table(
            self, 'Interaction100Table',
            table_name='Interaction100Table',
            partition_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        table_feed = dynamodb.Table(
            self, 'Feed100Table',
            table_name='Feed100Table',
            partition_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        user_pool = cognito.UserPool(
            self, "MovieUserPoolFinally",
            user_pool_name="MovieUserPoolFinally",
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_digits=True,
                require_lowercase=True,
                require_uppercase=True,
                require_symbols=False

            ),
            # AKO HOCEMO DA username mora @gmail.com otkomentarisati ovo
            sign_in_aliases=cognito.SignInAliases(email=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True)
            )
        )

        client = cognito.UserPoolClient(
            self, "MovieUserPoolClientFinally",
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

        admin_group = cognito.CfnUserPoolGroup(
            self, "AdminGroup",
            group_name="admin",
            user_pool_id=user_pool.user_pool_id,
            description="Admin group with elevated privileges"
        )

        # Kreiranje obične korisničke grupe
        user_group = cognito.CfnUserPoolGroup(
            self, "UserGroup",
            group_name="user",
            user_pool_id=user_pool.user_pool_id,
            description="Regular user group"
        )

        # Kreiranje SNS teme
        topic = sns.Topic(self, "MovieTopic",
                          display_name="MovieTopic",
                          topic_name="MovieTopic")

        actions_sns = [
            "sns:Publish",
            "sns:Subscribe"
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
                    "cognito-idp:AdminAddUserToGroup",
                    "cognito-idp:AdminRemoveUserFromGroup",
                    "cognito-idp:AdminGetUser",
                    "cognito-idp:AdminUpdateUserAttributes",
                    "sns:Publish",
                    "states:StartExecution",
                    "states:DescribeExecution",
                    "sns:Subscribe"
                ],
                resources=[
                    f"{bucket.bucket_arn}/*",
                    topic.topic_arn,
                    table.table_arn,
                    table_subscricions.table_arn,
                    table_review.table_arn,
                    table_download.table_arn,
                    table_interaction.table_arn,
                    table_feed.table_arn,
                    user_pool.user_pool_arn,
                ]
            )
        )

        def create_lambda_function(id, name, handler, include_dir, method, layers, database_dynamo, database_s3):
            env = 'TABLE_NAME'
            if database_dynamo is not None:
                database = database_dynamo
            else:
                if database_dynamo is None and database_s3 is None:
                    database = ""
                else:
                    env = 'BUCKET_NAME'
                    database = database_s3
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
                    "BUCKET_NAME": database_s3,
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

        get_single_movie_lambda = create_lambda_function(
            "getMovie",
            "getSingleMovieFuction",
            "getMovie.lambda_handler",
            "getMovie",
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

        download_record_lambda = create_lambda_function(
            "downloadRecord",
            "downloadRecordUser",
            "downloadRecord.download_record_handler",
            "downloadRecord",
            "POST",
            [],
            table.table_name,
            None
        )

        upload_data = create_lambda_function(
            "uploadMovieData",
            "uploadMovieS3Dynamo",
            "upload_data.upload_data_handler",
            "uploadMovies",
            "POST",
            [],
            table.table_name,
            bucket.bucket_name
        )

        edit_data = create_lambda_function(
            "editMovieData",
            "editMovie",
            "editMovie.edit_data_handler",
            "editMovie",
            "PUT",
            [],
            table.table_name,
            bucket.bucket_name
        )

        add_review_lambda = create_lambda_function(
            "addReviewFunction",
            "addReviewFunction",
            "addReviewHandler.add_review_handler",
            "addReview",
            "POST",
            [],
            table.table_name,
            None
        )

        search_lambda = create_lambda_function(
            "searchFunction",
            "searchFunction",
            "search.search_lambda_handler",
            "search",
            "POST",
            [],
            table.table_name,
            None
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

        get_subscribe_lambda = create_lambda_function(
            "getSubscribe",
            "getSubscribe",
            "subscribe.get_subscribes",
            "subscribe",
            "GET",
            [],
            table_subscricions.table_name,
            None
        )

        get_subscribe_lambda.add_to_role_policy(
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

        unsubscribe_lambda = create_lambda_function(
            "unsubscribe",
            "unsubscribe",
            "unsubscribe.lambda_handler",
            "unsubscribe",
            "DELETE",
            [],
            table_subscricions.table_name,
            None
        )

        get_transcoded_lambda = create_lambda_function(
            "getTranscodedFunction",
            "getTranscodedFunction",
            "getTranscodedVideo.lambda_handler",
            "getTranscodedVideo",
            "POST",
            [],
            None,
            bucket.bucket_name
        )

        # Dodajte dozvole za pristup DynamoDB tabeli
        unsubscribe_lambda.add_to_role_policy(
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

        get_transcoded_lambda.add_to_role_policy(
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

        delete_movie_lambda = create_lambda_function(
            "deleteMovie",
            "deleteMovie",
            "deleteMovie.lambda_handler",
            "deleteMovie",
            "DELETE",
            [],
            table.table_name,
            None
        )

        # Dodajte dozvole za pristup DynamoDB tabeli
        delete_movie_lambda.add_to_role_policy(
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
                    table.table_arn
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

        user_to_usergroup_lambda = create_lambda_function(
            "postToGroup",
            "toGroup",
            "user_to_group.lambda_handler",
            "userToUserGroup",
            "POST",
            [],
            table_subscricions.table_name,
            None
        )

        send_message_resolutions = create_lambda_function(
            "sendMessageTranscode",
            "sendMessageForTranscode",
            "sendTranscodeMessage.send_transcode_message_handler",
            "sendMessage",
            "POST",
            [],
            None,
            bucket.bucket_name
        )

        bucket.grant_read_write(send_message_resolutions)

        # Dodajte dozvole za pristup DynamoDB tabeli
        user_to_usergroup_lambda.add_to_role_policy(
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
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminSetUserPassword",
                    "cognito-idp:AdminAddUserToGroup"
                ],
                resources=[
                    table_subscricions.table_arn,
                    "arn:aws:cognito-idp:eu-central-1:992382767224:userpool/eu-central-1_0OImNFX7r"
                ]
            )
        )

        # # Lambda funkcije
        # first_lambda = lambda_.Function(
        #     self, "FirstLambda",
        #     runtime=lambda_.Runtime.PYTHON_3_9,
        #     handler="uploadS3handler.upload_S3_handler",
        #     code=lambda_.Code.from_asset("s3Upload")
        # )
        #
        # bucket.grant_read_write(first_lambda)
        #
        # second_lambda = lambda_.Function(
        #     self, "SecondLambda",
        #     runtime=lambda_.Runtime.PYTHON_3_9,
        #     handler="uploadDynamoHandler.upload_dynamo_handler",
        #     code=lambda_.Code.from_asset("dynamoUpload"),
        #     role=lambda_role
        # )
        #
        # start_upload_data = lambda_.Function(
        #     self, "StartUploadData",
        #     runtime=lambda_.Runtime.PYTHON_3_9,
        #     handler="startUploadMoviesHandler.upload_data_handler",
        #     code=lambda_.Code.from_asset("startUploadMovies"),
        #
        # )
        #
        # # Definisanje Step Function-a
        # first_task = tasks.LambdaInvoke(
        #     self, "First Task",
        #     lambda_function=first_lambda,
        #
        # )
        #
        # second_task = tasks.LambdaInvoke(
        #     self, "Second Task",
        #     lambda_function=second_lambda
        # )
        #
        # definition = second_task.next(first_task)
        #
        # state_machine = sfn.StateMachine(
        #     self, "StateMachine",
        #     definition=definition
        # )
        #
        # # Dodela dozvole Lambda funkciji da pokrene Step Function
        # state_machine.grant_start_execution(start_upload_data)
        # state_machine.grant_read(start_upload_data)
        # start_upload_data.add_environment('STATE_MACHINE_ARN', state_machine.state_machine_arn)

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

        my_layer = LayerVersion(self, 'Ffmpeg',
                                code=_lambda.Code.from_asset("layers/ffmpeg.zip"),
                                compatible_runtimes=[
                                    _lambda.Runtime.PYTHON_3_8,
                                    _lambda.Runtime.PYTHON_3_9,
                                    _lambda.Runtime.PYTHON_3_10,
                                    _lambda.Runtime.PYTHON_3_11
                                ],
                                description='A layer with the requests library'
                                )

        # Kreiraj Lambda funkciju koja koristi layer
        startStepLambda = _lambda.Function(self, 'TranscodeFunction',
                                           runtime=_lambda.Runtime.PYTHON_3_11,
                                           handler='stepFunc.transcode_step_func_handler',
                                           code=_lambda.Code.from_asset('transcodeStepFunc'),
                                           layers=[my_layer],
                                           timeout=Duration.seconds(900)
                                           )

        map_state = sfn.Map(self, 'Map State',
                            max_concurrency=3,
                            items_path=sfn.JsonPath.string_at('$.sharedData')
                            )

        map_state.add_retry(
            interval=Duration.seconds(5),
            max_attempts=5,
            backoff_rate=2.0
        )

        lambda_invoke_task = sfn_tasks.LambdaInvoke(self, 'Invoke Lambda',
                                                    lambda_function=startStepLambda,
                                                    timeout=Duration.seconds(1000)
                                                    )

        map_state.iterator(lambda_invoke_task)

        start_state = sfn.Pass(self, 'Start State')

        wait_state = sfn.Wait(self, 'Wait State',
                              time=sfn.WaitTime.duration(Duration.seconds(30)))

        definition = wait_state.next(map_state)

        state_machine = sfn.StateMachine(self, 'StateMachineTranscode',
                                         definition=definition,
                                         timeout=Duration.minutes(15)
                                         )

        #
        state_machine.grant_start_execution(send_message_resolutions)

        sqs_queue_arn = 'arn:aws:sqs:eu-central-1:992382767224:CloudBackStack-UploadSQS4BB1896E-T93YQkfluhSC'
        sqs_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=['sqs:SendMessage'],
            resources=[sqs_queue_arn]
        )

        send_message_resolutions.add_to_role_policy(sqs_policy_statement)

        bucket.grant_read(startStepLambda)
        bucket.grant_put(startStepLambda)
        bucket.grant_read_write(startStepLambda)

        # Postavljanje okruženja za uploadMovie Lambda funkciju
        send_message_resolutions.add_environment('STEP_FUNCTION_ARN', state_machine.state_machine_arn)
        # RUCNO DODAMO ADRESU OD STEP FUNKCIJE

        # Postavljanje okruženja za transcodeContent Lambda funkciju
        # transcode_content.add_environment('BUCKET_NAME', props.bucket_name)
        # OVO CEMO RUCNO

        # SQS Queue
        sqs_queue = sqs.Queue(self, "UploadSQS")

        # Lambda funkcija - Step Function Invoker
        step_function_invoker = _lambda.Function(self, "StepFunctionInvoker",
                                                 runtime=_lambda.Runtime.PYTHON_3_11,
                                                 handler="invokeStepFunc.invoke_step_func_handler",
                                                 code=_lambda.Code.from_asset("invokeStepFunc"),
                                                 timeout=Duration.seconds(30)
                                                 )

        sqs_queue.grant_send_messages(step_function_invoker)
        bucket.grant_read(step_function_invoker)

        bucket.grant_read_write(upload_data)
        bucket.grant_read_write(edit_data)

        step_function_invoker.add_environment("STATE_MACHINE_ARN", state_machine.state_machine_arn)
        state_machine.grant_start_execution(step_function_invoker)

        # bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(step_function_invoker))
        step_function_invoker.add_event_source(lambda_event_sources.SqsEventSource(sqs_queue))

        # Dodavanje dozvola Lambda funkciji za pristup DynamoDB tabeli
        table.grant_read_data(get_movie_lambda)

        bucket.grant_read_write(upload_data)
        bucket.grant_read_write(edit_data)
        bucket.grant_read_write(get_transcoded_lambda)

        # Dodavanje dozvola Lambda funkciji za pristup DynamoDB tabeli
        table.grant_read_data(get_movie_lambda)
        table.grant_read_data(get_single_movie_lambda)
        table.grant_read_data(download_record_lambda)
        table.grant_read_data(add_review_lambda)
        table.grant_read_data(search_lambda)
        table.grant_read_data(delete_movie_lambda)


        table_subscricions.add_global_secondary_index(
            index_name='subscriber-index4',
            partition_key={'name': 'subscriber', 'type': dynamodb.AttributeType.STRING}
        )
        # table_subscricions.add_global_secondary_index(
        #     index_name='subscriber-index',
        #     partition_key={'name': 'subscriber', 'type': dynamodb.AttributeType.STRING}
        # )
        table_subscricions.grant_read_write_data(subscribe_lambda)
        table_subscricions.grant_read_write_data(get_subscribe_lambda)
        table_subscricions.grant_read_write_data(unsubscribe_lambda)

        table_review.add_global_secondary_index(
            index_name='review-index-review',
            partition_key={'name': 'user_id', 'type': dynamodb.AttributeType.STRING},
            # sort_key={'name': 'rate', 'type': dynamodb.AttributeType.STRING}  # Dodavanje sort key-a
        )
        table_subscricions.grant_read_write_data(put_interaction_lambda)
        table_subscricions.grant_read_write_data(user_to_usergroup_lambda)
        table.grant_read_write_data(edit_data)

        table_review.grant_read_write_data(put_interaction_lambda)

        table.add_global_secondary_index(
            index_name='AllAttributesIndex10',
            partition_key={'name': 'all_attributes', 'type': dynamodb.AttributeType.STRING},
            # sort_key={'name': 'movie_id', 'type': dynamodb.AttributeType.STRING},
            projection_type=dynamodb.ProjectionType.ALL
        )

        bucket.grant_read_write(download_movie_lambda)
        bucket.grant_read_write(subscribe_lambda)
        bucket.grant_read_write(put_interaction_lambda)
        bucket.grant_read_write(get_feed_lambda)
        bucket.grant_read_write(user_to_usergroup_lambda)
        bucket.grant_read_write(get_subscribe_lambda)
        bucket.grant_read_write(unsubscribe_lambda)

        self.api = apigateway.RestApi(self, "CloudProjectTeam14",
                                      rest_api_name="CloudProject2023",
                                      description="This service serves movie contents.",
                                      endpoint_types=[apigateway.EndpointType.REGIONAL],
                                      default_cors_preflight_options={
                                          "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                          "allow_methods": apigateway.Cors.ALL_METHODS
                                      }
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

        send_message_resolutions.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        upload_data.add_permission(
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

        get_subscribe_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        unsubscribe_lambda.add_permission(
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

        get_single_movie_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        download_record_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        user_to_usergroup_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        edit_data.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        add_review_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        search_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        get_transcoded_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        search_lambda.add_to_role_policy(
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
                    table.table_arn
                ]
            )
        )
        delete_movie_lambda.add_permission(
            "ApiGatewayInvokePermission",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            source_arn=self.api.arn_for_execute_api("/*/*/*")
        )

        # AUTORIZACIJA GLUPAVA
        # npr user ima pravo na subscribe a admin na upload pa to moramo srediti
        # DODAO SAM ZA USERA SUBSCRIBE DA MOZE ADMIN NE
        # ADMIN MOZE UPLOAD USER NE

        authorization_user_lambda_function = create_lambda_function(
            "authorization_user",
            "AuthorizationFunctionUser",
            "authorization.user_permission_handler",
            "authorization",
            "POST",
            [],
            table.table_name,
            None
        )

        authorization_admin_lambda_function = create_lambda_function(
            "authorization_admin",
            "AuthorizationFunctionAdmin",
            "authorization.admin_permission_handler",
            "authorization",
            "POST",
            [],
            table.table_name,
            None
        )

        authorization_admin_lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["iam:GetRolePolicy",
                         "dynamodb:GetItem",
                         "dynamodb:Query",
                         "dynamodb:Scan",
                         "s3:GetObject",
                         "s3:ListBucket",
                         "cognito-idp:AdminCreateUser",
                         "cognito-idp:AdminInitiateAuth",
                         "cognito-idp:AdminRespondToAuthChallenge",
                         "cognito-idp:InitiateAuth",
                         "cognito-idp:RespondToAuthChallenge",
                         "cognito-idp:AdminGetUser",
                         "cognito-idp:GlobalSignOut",
                         "cognito-idp:AdminAddUserToGroup",
                         "cognito-idp:AdminListGroupsForUser",
                         "iam:ListAttachedRolePolicies",
                         "iam:ListRolePolicies",
                         "iam:GetRolePolicy",
                         "sns:Subscribe",
                         "sns:ListSubscriptionsByTopic"
                         ],
                resources=[table.table_arn,
                           user_pool.user_pool_arn,
                           f"arn:aws:cognito-idp:{self.region}:{self.account}:userpool/{user_pool.user_pool_id}",
                           ]
            )
        )

        authorization_user_lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["iam:GetRolePolicy",
                         "dynamodb:GetItem",
                         "dynamodb:Query",
                         "dynamodb:Scan",
                         "s3:GetObject",
                         "s3:ListBucket",
                         "cognito-idp:AdminCreateUser",
                         "cognito-idp:AdminInitiateAuth",
                         "cognito-idp:AdminRespondToAuthChallenge",
                         "cognito-idp:InitiateAuth",
                         "cognito-idp:RespondToAuthChallenge",
                         "cognito-idp:AdminGetUser",
                         "cognito-idp:GlobalSignOut",
                         "cognito-idp:AdminAddUserToGroup",
                         "cognito-idp:AdminListGroupsForUser",
                         "iam:ListAttachedRolePolicies",
                         "iam:ListRolePolicies",
                         "iam:GetRolePolicy",
                         "sns:Subscribe",
                         "sns:ListSubscriptionsByTopic"
                         ],
                resources=[table.table_arn,
                           user_pool.user_pool_arn,
                           f"arn:aws:cognito-idp:{self.region}:{self.account}:userpool/{user_pool.user_pool_id}",
                           ]
            )
        )

        authorizer_admin = apigateway.TokenAuthorizer(
            self, "AdminAuthorizer",
            handler=authorization_admin_lambda_function
        )
        #
        # authorizer_user = apigateway.TokenAuthorizer(
        #     self, "UserAuthorizer",
        #     handler=authorization_user_lambda_function
        # )

        movie_resource = self.api.root.add_resource("movieNew")

        # GET metoda za /movies123
        get_movies_integration = apigateway.LambdaIntegration(get_movie_lambda, credentials_role=api_gateway_role,
                                                              proxy=True)
        self.api.root.add_resource("movies123").add_method("GET", get_movies_integration)

        # POST metoda za /movie
        movie_resource = self.api.root.add_resource("movie")
        movie_resource.add_method("POST", apigateway.LambdaIntegration(upload_data, credentials_role=api_gateway_role,
                                                                       proxy=True))

        # POST metoda za /movieS3
        self.api.root.add_resource("movieS3").add_method("POST", apigateway.LambdaIntegration(upload_data,
                                                                                              credentials_role=api_gateway_role,
                                                                                              proxy=True),authorizer=authorizer_admin)

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

        get_subscribe_resource = self.api.root.add_resource("getSubscribe")
        username_resource = get_subscribe_resource.add_resource("{username}")
        username_resource.add_method("GET",
                                     apigateway.LambdaIntegration(get_subscribe_lambda,
                                                                  credentials_role=api_gateway_role, proxy=True))

        unsubscribe_resource = self.api.root.add_resource("unsubscribe")
        unsub_resource = unsubscribe_resource.add_resource("{subscription_id}")
        unsub_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(unsubscribe_lambda, credentials_role=api_gateway_role, proxy=True))

        delete_movie_resource = self.api.root.add_resource("deleteMovie")
        delete_resource = delete_movie_resource.add_resource("{movie_id}")
        delete_resource.add_method("DELETE",
                                   apigateway.LambdaIntegration(delete_movie_lambda,
                                                                credentials_role=api_gateway_role, proxy=True))

        add_user_to_group_resource = self.api.root.add_resource("toGroup")
        add_user_to_group_resource.add_method("POST",
                                              apigateway.LambdaIntegration(user_to_usergroup_lambda,
                                                                           credentials_role=api_gateway_role,
                                                                           proxy=True))

        interaction_resource = self.api.root.add_resource("interaction")
        interaction_resource.add_method("PUT",
                                        apigateway.LambdaIntegration(put_interaction_lambda,
                                                                     credentials_role=api_gateway_role,
                                                                     proxy=True))

        new_rute = self.api.root.add_resource("getFromS3")
        new_rute_id = new_rute.add_resource("{id}")
        new_rute_id.add_method("GET", apigateway.LambdaIntegration(download_movie_lambda, proxy=True))

        new_rute_single = self.api.root.add_resource("getSingleMovie")
        new_rute_single_id = new_rute_single.add_resource("{id}")
        new_rute_single_id.add_method("GET", apigateway.LambdaIntegration(get_single_movie_lambda, proxy=True))

        download_record = self.api.root.add_resource("downloadRecordUser")
        download_record.add_method("POST",
                                   apigateway.LambdaIntegration(download_record_lambda,
                                                                credentials_role=api_gateway_role,
                                                                proxy=True))

        add_review = self.api.root.add_resource("addReviewFunction")
        add_review.add_method("POST",
                              apigateway.LambdaIntegration(add_review_lambda,
                                                           credentials_role=api_gateway_role,
                                                           proxy=True))

        search = self.api.root.add_resource("search")
        search.add_method("POST",
                          apigateway.LambdaIntegration(search_lambda,
                                                       credentials_role=api_gateway_role,
                                                       proxy=True))

        get_feed = self.api.root.add_resource("feed").add_resource("{user_id}")
        get_feed.add_method("GET",
                            apigateway.LambdaIntegration(get_feed_lambda,
                                                         credentials_role=api_gateway_role,
                                                         proxy=True))

        self.api.root.add_resource("putMovie").add_method("PUT", apigateway.LambdaIntegration(edit_data,
                                                                                              credentials_role=api_gateway_role,
                                                                                              proxy=True))

        # send_message_resolutions
        search = self.api.root.add_resource("sendMessageTranscode")
        search.add_method("POST",
                          apigateway.LambdaIntegration(send_message_resolutions,
                                                       credentials_role=api_gateway_role,
                                                       proxy=True))

        get_transcoded = self.api.root.add_resource("transcoding")
        get_transcoded.add_method("POST",
                          apigateway.LambdaIntegration(get_transcoded_lambda,
                                                       credentials_role=api_gateway_role,
                                                       proxy=True))
        # deployment nakon dodavanja svih resursa i metoda
        api_deployment_new = apigateway.Deployment(self, "ApiDeploymentTotalNew",
                                                   api=self.api)

        # novi stage
        apigateway.Stage(self, "NewStage",
                         deployment=api_deployment_new,
                         stage_name="noviStage")
