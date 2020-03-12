import boto3
from os import environ

from src import logger
from src.messages import Message


queue_name = environ['TARGET_QUEUE_NAME']


def entry_point(events, context):
    messages_to_send = events['messages_to_send']
    logger.info(f"Running profile with {messages_to_send} messages")
    sqs_client = initialise_client()
    broadcast_messages(sqs_client, messages_to_send)
    logger.info("Invocation complete, ending")


def initialise_client():
    return boto3.client('sqs')


def broadcast_messages(sqs_client, messages_to_send):
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    for each in range(0, messages_to_send):
        message = Message().dict
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
