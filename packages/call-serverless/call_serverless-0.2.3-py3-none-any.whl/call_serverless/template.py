_BASE_TEMPLATE = {
    "resource": "",
    "path": "",
    "httpMethod": "GET",
    "headers": None,
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": None,
    "requestContext": {
        "resourcePath": "",
        "httpMethod": "GET",
        "path": "",
        "protocol": "HTTP/1.1",
        "stage": "",
    },
    "body": None,
    "isBase64Encoded": False,
}


def base_template():
    return _BASE_TEMPLATE.copy()
