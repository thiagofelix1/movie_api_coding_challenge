from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from application.authorization import  validate_token_authorization_api
from rest_framework.exceptions import APIException
from rest_framework import status

class IsAuthenticated(permissions.BasePermission):
    """
    Custom Permission to check user authenticated
    """
    def has_permission(self, request, view):
        if not 'HTTP_TOKEN' in request.META:
            return False
        response_token_validate = validate_token_authorization_api(data={'token': request.META['HTTP_TOKEN']})

        if 'error' in response_token_validate:
            raise ErrorConnectionAuthorizationApi()

        if 'valid token' in response_token_validate:
            return response_token_validate['valid token']

class IsUserBasicPermissions(permissions.BasePermission):
    """
    Custom Permission to check user is basic or superior
    """
    message = "invalid login credentials"
    def has_permission(self, request, view):
        if not 'HTTP_TOKEN' in request.META:
            return False
        response_token_validate = validate_token_authorization_api(data={'token':request.META['HTTP_TOKEN']})
        if 'error' in response_token_validate:
            raise ErrorConnectionAuthorizationApi()
        if 'valid token' in response_token_validate:
            if response_token_validate['valid token']:
                if response_token_validate['profile'] != 'reader':
                    return True
                raise NotPermission()
            raise TokenNotExists()

class IsUserAdvancedPermissions(permissions.BasePermission):
    """
    Custom Permission to check user is advanced or superior
    """
    message = "invalid login credentials"
    def has_permission(self, request, view):
        if not 'HTTP_TOKEN' in request.META:
            return False
        response_token_validate = validate_token_authorization_api(data={'token':request.META['HTTP_TOKEN']})
        if 'error' in response_token_validate:
            raise ErrorConnectionAuthorizationApi()
        if 'valid token' in response_token_validate:
            if response_token_validate['valid token']:
                if response_token_validate['profile'] != 'reader' and response_token_validate['profile'] != 'basic':
                    return True
                raise NotPermission()
            raise TokenNotExists()


class IsUserModeratorPermissions(permissions.BasePermission):
    """
    Custom Permission to check user is moderator
    """
    def has_permission(self, request, view):
        if not 'HTTP_TOKEN' in request.META:
            return False
        response_token_validate = validate_token_authorization_api(data={'token':request.META['HTTP_TOKEN']})
        if 'error' in response_token_validate:
            raise ErrorConnectionAuthorizationApi()
        if 'valid token' in response_token_validate:
            if response_token_validate['valid token']:
                if response_token_validate['profile'] != 'reader' and response_token_validate['profile'] != 'basic' and response_token_validate['profile'] != 'advanced':
                    return True
                raise NotPermission()
            raise TokenNotExists()

class TokenNotExists(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'invalid token'}
    default_code = 'not_access'

class NotPermission(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'user does not have access'}
    default_code = 'not_access'

class ErrorConnectionAuthorizationApi(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {'error': True, 'message': 'Authorization Service connection error'}
    default_code = 'not_access'