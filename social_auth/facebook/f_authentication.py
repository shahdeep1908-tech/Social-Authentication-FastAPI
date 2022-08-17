import json
import os

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from social_auth import oauth
from dotenv import load_dotenv
from social_auth.google import services

load_dotenv()

router = APIRouter(
    tags=["Authentication"]
)

oauth.register(
        name='facebook',
        client_id=os.environ.get('FACEBOOK_CLIENT_ID'),
        client_secret=os.environ.get('FACEBOOK_CLIENT_SECRET'),
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
)


@router.get('/facebook')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/facebook/logout">Logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/facebook/login">Facebook Login</a>')


@router.get('/facebook/login')
async def login(request: Request):
    redirect_uri = request.url_for('facebook_auth')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


@router.get('/facebook/auth')
async def facebook_auth(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    print('+++++++++++++++++++++++++++++++++++++++++')
    print(token)
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    user = resp.json()
    if user:
        request.session['user'] = dict(user)
    print("Facebook User ", user)
    return RedirectResponse(url='/facebook')


@router.get('/facebook/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/facebook')