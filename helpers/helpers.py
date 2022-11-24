from rest_framework.exceptions import ValidationError


def check_response(response, detail):
    if response.status_code != 200:
        raise ValidationError(
            detail=detail if detail is not None else response.error, code=response.status_code)


def gen_url(url, params):
    query_strings = []
    for key, value in params.items():

        query_strings.append('{}={}'.format(
            key, ",".join(value) if type(value) == list else value))
    return url + '?' + '&'.join(query_strings)
