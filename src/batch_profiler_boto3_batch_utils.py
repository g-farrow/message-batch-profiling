from os import environ
from aws_xray_sdk.core import xray_recorder
from boto3_batch_utils import SQSBatchDispatcher, KinesisBatchDispatcher

from src import logger
from src.messages import Message


sqs_client = SQSBatchDispatcher(environ['TARGET_QUEUE_NAME'])
kinesis_client = KinesisBatchDispatcher(environ['TARGET_STREAM_NAME'])


@xray_recorder.capture()
def entry_point(events, context):
    messages_to_send = events['messages_to_send']
    logger.info(f"Running profile with {messages_to_send} messages")
    messages_list = [Message() for each in range(0, messages_to_send)]
    if events['sqs'].upper() == "TRUE" and messages_to_send <= 10:
        broadcast_messages_sqs(messages_list)
    if events['kinesis'].upper() == "TRUE":
        broadcast_messages_kinesis(messages_list)
    logger.info("Invocation complete, ending")


@xray_recorder.capture()
def broadcast_messages_sqs(messages_list):
    for message in messages_list:
        sqs_client.submit_payload(message.dict)
    sqs_client.flush_payloads()


@xray_recorder.capture()
def broadcast_messages_kinesis(messages_list):
    for message in messages_list:
        kinesis_client.submit_payload(message.dict)
    sqs_client.flush_payloads()
