from core.models import TeamsToken, PoolToken
from typing import Callable
from django.core.exceptions import PermissionDenied


MS_TEAMS_CONTENT_SECURITY_POLICY = (
    'frame-ancestors teams.microsoft.com '
    '*.teams.microsoft.com *.skype.com'
)


def teams_tab_view(func):
    """
    Sets Content-Security-Policy header and legacy
    X-Content-Security-Policy for MS Teams
    """
    
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['Content-Security-Policy'] = MS_TEAMS_CONTENT_SECURITY_POLICY
        response['X-Content-Security-Policy'] = MS_TEAMS_CONTENT_SECURITY_POLICY
        return response
    
    return wrapper


def validate_query_token(is_valid: Callable[[str], bool]):
    """
    Checks token from query parameter or form parameter
    with validator function
    """
    
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            token = request.GET.get('token') or request.POST.get('token')
            if is_valid(token):
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied('Invalid token')
        return wrapper
    return decorator


validate_teams_token = validate_query_token(
    lambda token: TeamsToken.objects.filter(token=token).exists()
)


validate_pool_token = validate_query_token(
    lambda pool_token: PoolToken.objects.filter(token=pool_token).exists()
)