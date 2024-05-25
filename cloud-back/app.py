#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloud_back.cloud_back_stack import CloudBackStack


app = cdk.App()
CloudBackStack(app, "CloudBackStack",

            )

app.synth()
