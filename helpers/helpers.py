from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

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

def gen_auth_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }