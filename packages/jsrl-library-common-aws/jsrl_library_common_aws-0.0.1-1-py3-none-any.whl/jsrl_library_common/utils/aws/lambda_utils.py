import boto3

def send_lambda_message(function_name, 
                        payload,
                        invocation_type='Event',
                        lambda_client=None):
    """Invoke lambda with specific payload

    Args:
        - function_name (string): the lambda function name
        - payload (string|json): the payload to send 
        - invocation_type (string): the invoke type. Default 'Event'
        - lambda_client (boto3.Lambda.Client): the lambda client if exists
    """
    client = _get_lambda_connection(lambda_client)

    response = client.invoke(FunctionName=function_name,
                             InvocationType=invocation_type,
                             Payload=payload)
    return response


def _get_lambda_connection(lambda_client=None):
    """Get the step function connection

    Args:
        - lambda_client (boto3.client): the lambda client if exists

    Returns:
        boto3.client: the lambda client
    """
    client = None
    if (lambda_client):
        client = lambda_client
    else:
        client = boto3.client('lambda')
    return client