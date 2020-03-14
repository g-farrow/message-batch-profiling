import boto3
from aws_xray_sdk.core import xray_recorder
from os import environ

from src import logger
from src.messages import Message


queue_name = environ['TARGET_QUEUE_NAME']
stream_name = environ['TARGET_STREAM_NAME']


@xray_recorder.capture()
def entry_point(events, context):
    messages_to_send = events['messages_to_send']
    logger.info(f"Running profile with {messages_to_send} messages")
    sqs_client, kinesis_client = initialise_clients()
    messages_list = [Message() for each in range(0, messages_to_send)]
    if events['sqs'].upper() == "TRUE" and messages_to_send <= 10:
        broadcast_messages_sqs(sqs_client, messages_list)
    if events['kinesis'].upper() == "TRUE":
        broadcast_messages_kinesis(kinesis_client, messages_list)
    logger.info("Invocation complete, ending")


@xray_recorder.capture()
def initialise_clients():
    return boto3.client('sqs'), boto3.client('kinesis')


@xray_recorder.capture()
def broadcast_messages_sqs(sqs_client, messages_list):
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    for message in messages_list:
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message.str
        )


@xray_recorder.capture()
def broadcast_messages_kinesis(kinesis_client, messages_list):
    for message in messages_list:
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=message.str,
            PartitionKey=str(message.id)
        )
