import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud_back.cloud_back_stack import CloudBackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud_back/cloud_back_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudBackStack(app, "cloud-back")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
