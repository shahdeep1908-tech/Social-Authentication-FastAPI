import pyshorteners
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from social_auth import oauth, models


router = APIRouter(
    tags=["Authentication"]
)

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
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/google/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    # print(user)
    # print(user['picture'])
    user_data = models.User.check_user_exists(user['email'])
    if user_data:
        return {'status_code': 200,
                'msg': 'User Exists! Login Successful'}
    else:
        new_user = models.User.create_user(str(user['sub']), user['name'], user['email'], user['picture'])
        if new_user:
            return {'status_code': 200,
                    'msg': 'New User Created! Login Successful'}
        else:
            return RedirectResponse(url='/')
