# message-batch-profiling
Simple system for profiling performance differences between message broadcast APIs. Accompanying code to the blog post
which can be found [here](#TODO)

# Deployment
Deployment uses Github actions and is very easy to set up. All you need is a deployment user in your AWS account:
* Fork [this repo](https://github.com/g-farrow/message-batch-profiling) in your Github account.
* Add a [new IAM policy](https://console.aws.amazon.com/iam/home?region=eu-west-1#/policies) in you AWS account. The 
policy should use the permissions provided in 
[`resources/deployment_role.json`](https://github.com/g-farrow/message-batch-profiling/blob/master/resources/deployment_role.json).
* Create a [new user](https://console.aws.amazon.com/iam/home?region=eu-west-1#/users) for deployment purposes, add the 
policy you created in the previous step. _Note: the user only requires programmatic access_
* Copy out the Access Key and Secret key.
* Go to your forked repository in Github, choose Settings > Secrets and add the following:
  * AWS_ACCESS_KEY_ID
  * AWS_SECRET_ACCESS_KEY
* Create a new commit on the master branch (make a dummy change to the README for example) - this will trigger the 
Github actions pipeline and deploy the stack.

## Resources:
Other than the resources required for deployment, the following AWS Resources will be provisioned:
* Lambda:
  * BatchProfilerIndividual
  * BatchProfilerBatch
  * BatchProfilerBoto3BatchUtils
* SQS Queue:
  * message-batch-profiling-TargetQueue

# Running the tests
To run the tests you can use AWS Lambda's in-built "Test Events" functionality. Setup tests against each of the deployed
Lambda Functions:
```json
{
  "messages_to_send": 10,
  "sqs": "True",
  "kinesis": "False"
}
```
Running this test will cause the Lambda to send the requested number of messages to the SQS queue. **Note:** A maximum 
of 10 should be used.