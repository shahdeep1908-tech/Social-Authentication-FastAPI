from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from social_auth import oauth
from social_auth.google import services


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


@router.get('/google')
async def homepage(request: Request):
    service_obj = services.Google(request)
    return service_obj.homepage()


@router.route('/google/login')
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
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/google')


@router.get('/google/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/google')
