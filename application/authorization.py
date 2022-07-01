import requests
import json
from rest_framework.response import Response
from rest_framework import status

KEY_AUTH_API = 'e907826fa8b7e7899f48516b2a6758be'
HEADER_REQUEST_AUTH = {
    'token': KEY_AUTH_API
}
def sign_up_authorization_api(data):
    url = 'http://127.0.0.1:8000/signup'
    try:
        req = requests.request("POST", url, data=data, headers=HEADER_REQUEST_AUTH , verify=False)
        return {'response': json.loads(req.text), 'status': req.status_code}
    except:
        return {'response': 'Authorization Service connection error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}


def sign_in_authorization_api(data):
    url = 'http://127.0.0.1:8000/api-token-auth/'
    try:
        req = requests.request("POST", url, data=data, headers=HEADER_REQUEST_AUTH , verify=False)
        return {'response': json.loads(req.text), 'status': req.status_code}
    except:
        return {'response': 'Authorization Service connection error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}


def validate_token_authorization_api(data):
    url = 'http://127.0.0.1:8000/api-token-valid/'
    try:
        req = requests.request("POST", url, data=data, headers=HEADER_REQUEST_AUTH , verify=False)
        return json.loads(req.text)
    except:
        return {'error': 'Authorization Service connection error', 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}



def add_points_user(data):
    url = 'http://127.0.0.1:8000/add-points/'
    req = requests.request("POST", url, data=data, headers=HEADER_REQUEST_AUTH , verify=False)
    return json.loads(req.text)


def make_moderator(data):
    url = 'http://127.0.0.1:8000/make-moderator/'
    req = requests.request("POST", url, data=data, headers=HEADER_REQUEST_AUTH , verify=False)
    print(req.status_code)
    return {
        'response': json.loads(req.text),
        'status': req.status_code
    }
