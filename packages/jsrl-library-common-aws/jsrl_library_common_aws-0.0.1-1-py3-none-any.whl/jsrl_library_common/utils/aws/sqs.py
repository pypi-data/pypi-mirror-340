import json
import boto3
from botocore.exceptions import ClientError

def get_queue_url(queue_arn, sqs_client=None):
    """Get queue url from queue arn
    
    Args:
        - queue_arn (string): arn of sqs queue
        - sqs_client (boto3.client): the sqs client if exists
        
    Returns:
        - string: queue url associated to queue arn
        - boto3.client: the sqs client
    """
    account_id, queue_name = queue_arn.split(':')[-2:]
    client = _get_sqs_connection(sqs_client)
                                 
    url = client.get_queue_url(QueueName=queue_name,
                               QueueOwnerAWSAccountId=account_id)
    
    return url["QueueUrl"], client


def delete_queue_message(queue_url, 
                         receipt_handle,
                         sqs_client=None):
    """Delete specific message from queue
    
    Args:
        - queue_url (string): the sqs url
        - receipt_handle (string): the receipt handle of message
        - sqs_client (boto3.client): the sqs client if exists
        
    Returns:
        - boto3.client: the sqs client 
    """
    try:
        client = _get_sqs_connection(sqs_client)
                                     
        client.delete_message(QueueUrl=queue_url,
                              ReceiptHandle=receipt_handle)
        return client
    except ClientError:
        raise Exception(f'Could not delete the meessage from the - {queue_url}')
    except Exception as ex:
        raise ex
    

def send_message_to_sqs_queue(queue_url,
                              payload,
                              sqs_client=None):
    """Send the payload to sqs queue

    Args:
        - queue_url (string): the queue url
        - payload (string|dict): the message will be sent
        - sqs_client (boto3.client): the sqs client if exists
    
    Returns:
        - dict: the boto3 send message response
    """
    message = payload if type(payload) is str \
                      else json.dumps(payload)
    
    client = _get_sqs_connection(sqs_client)
    
    response = client.send_message(QueueUrl=queue_url,
                                   MessageBody=message)

    return response


def _get_sqs_connection(sqs_client=None):
    """Get the sqs connection

    Args:
        - sqs_client (boto3.client): the sqs client if exists

    Returns:
        boto3.client: the sqs client
    """
    client = None
    if (sqs_client):
        client = sqs_client
    else: 
        client = boto3.client('sqs')
    return client