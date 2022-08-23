from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth
from dotenv import load_dotenv
from social_auth import models
import pyshorteners
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

load_dotenv()

router = APIRouter(
    tags=["Authentication"]
)

oauth.register(
    name='facebook',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email'},
)


@router.get('/facebook/login')
async def login(request: Request):
    redirect_uri = request.url_for('facebook_auth')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


@router.get('/facebook/auth')
async def facebook_auth(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    url = 'https://graph.facebook.com/me?fields=id,name,email,picture{url}'
    resp = await oauth.facebook.get(url, token=token)
    user = resp.json()

    user_data = models.User.check_user_exists(user['email'])
    if user_data:
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['login'])})
    else:
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(user['picture']['data']['url'])
        new_user = models.User.create_user(user['id'], user['name'], user['email'], short_url)
        if new_user:
            return JSONResponse({'status_code': 200,
                                 'msg': 'New User Created! Login Successful',
                                 'access_token': create_token(user['login'])})
        else:
            return RedirectResponse(url='/')
