from os import environ
from aws_xray_sdk.core import xray_recorder
from boto3_batch_utils import SQSBatchDispatcher

from src import logger
from src.messages import Message


sqs_client = SQSBatchDispatcher(environ['TARGET_QUEUE_NAME'])


@xray_recorder.capture()
def entry_point(events, context):
    messages_to_send = events['messages_to_send']
    logger.info(f"Running profile with {messages_to_send} messages")
    broadcast_messages(sqs_client, messages_to_send)
    logger.info("Invocation complete, ending")


@xray_recorder.capture()
def broadcast_messages(sqs_client, messages_to_send):
    messages_list = [Message() for each in range(0, messages_to_send)]
    for message in messages_list:
        sqs_client.submit_payload(message.dict)
    sqs_client.flush_payloads()
