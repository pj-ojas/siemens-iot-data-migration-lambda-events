import json

# import requests

from stream_processor import StreamProcessor


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    result = False
    try:
        stream_processor = StreamProcessor()
        result = stream_processor.process(event)
    except Exception as e:
        # Send some context about this error to Lambda Logs
        print("Exception: app.py: lambda_handler", e)
        raise e
    if result == True:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "lambda success",
            }),
        }
    else:
        print("failed")
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "something wrong in lamda"})
        }
