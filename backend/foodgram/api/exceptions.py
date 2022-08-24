from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    for key, item in response.data.items():
        if isinstance(item, list):
            response.data[key] = " ".join(elem.title() for elem in item)

    return response
