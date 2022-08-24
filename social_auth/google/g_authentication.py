from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from social_auth import oauth, models
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

"""
Google Login Route: It contains 2 routes /login and /auth routes.
/login route redirect homepage to google authentication page.
/auth route goes to google login page to fetch access token and further user_data.
"""

router = APIRouter(
    tags=["Authentication"]
)

"""Below is google registration urls"""
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/google/login')
async def login(request: Request):
    """
    Creates redirect url and pass to auth function.
    :param request: Request object - Fetch user request token.
    :return: oauth redirect url
    """
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/google/auth')
async def auth(request: Request):
    """
    Redirect to google login page and create access token and fetch userdata.
    :param request: Request object - Fetch user request token.
    :return: Json Object - login-user access_token.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

    user = token.get('userinfo')

    user_data = models.User.check_user_exists(user['email'])
    if user_data:
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['email'])})
    else:
        new_user = models.User.create_user(str(user['sub']), user['name'], user['email'], user['picture'])
        if new_user:
            return JSONResponse({'status_code': 200,
                                 'msg': 'New User Created! Login Successful',
                                 'access_token': create_token(user['email'])})
        else:
            return RedirectResponse(url='/')
