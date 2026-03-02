from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """Wrap DRF's default exception handler to provide a consistent error format."""
    response = drf_exception_handler(exc, context)
+
    if response is not None:
        # Transform to {"errors": [...]}
        data = response.data
        errors = []
        if isinstance(data, dict):
            for k, v in data.items():
                # v may be list of strings or single string
                if isinstance(v, list):
                    for item in v:
                        errors.append({'field': k, 'message': str(item)})
                else:
                    errors.append({'field': k, 'message': str(v)})
        else:
            errors.append({'message': str(data)})

        response.data = {'errors': errors}

    return response
