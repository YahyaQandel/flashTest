from rest_framework.authtoken.models import Token
TOKEN_TYPE = 'Bearer'


def get_request_authentication_headers(user):
    user_token = Token.objects.get(user_id=user.id)
    request_headers = {'HTTP_AUTHORIZATION': '{} {}'.format(TOKEN_TYPE, user_token)}
    return request_headers
