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
    messages_list = [Message() for each in range(0, messages_to_send)]
    sqs_client, kinesis_client = initialise_clients()
    if events['sqs'] and messages_to_send <= 10:
        broadcast_messages_sqs(sqs_client, messages_list)
    if events['kinesis']:
        broadcast_messages_kinesis(kinesis_client, messages_list)
    logger.info("Invocation complete, ending")


@xray_recorder.capture()
def initialise_clients():
    return boto3.client('sqs'), boto3.client('kinesis')


@xray_recorder.capture()
def broadcast_messages_sqs(sqs_client, messages_list):
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    sqs_client.send_message_batch(
        QueueUrl=queue_url,
        Entries=[{'Id': message.id, 'MessageBody': message.str} for message in messages_list]
    )


@xray_recorder.capture()
def broadcast_messages_kinesis(kinesis_client, messages_list):
    kinesis_client.put_records(
        StreamName=stream_name,
        Records=[
            {'Data': message.str, 'PartitionKey': str(message.id)} for message in messages_list
        ]
    )