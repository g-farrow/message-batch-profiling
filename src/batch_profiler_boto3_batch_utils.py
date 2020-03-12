from os import environ
from boto3_batch_utils import SQSBatchDispatcher

from src import logger
from src.messages import Message


sqs_client = SQSBatchDispatcher(environ['TARGET_QUEUE_NAME'])


def entry_point(events, context):
    messages_to_send = events['messages_to_send']
    logger.info(f"Running profile with {messages_to_send} messages")
    broadcast_messages(sqs_client, messages_to_send)
    sqs_client.flush_payloads()
    logger.info("Invocation complete, ending")


def broadcast_messages(sqs_client, messages_to_send):
    for each in range(0, messages_to_send):
        sqs_client.submit_payload(Message().dict)
