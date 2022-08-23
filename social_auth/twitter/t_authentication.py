from typing import Any

import pyshorteners
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token


router = APIRouter(
    tags=["Authentication"]
)

oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)


@router.get('/twitter/login')
async def login(request: Request) -> Any:
    redirect_uri = request.url_for('twitter_auth')
    return await oauth.twitter.authorize_redirect(request, redirect_uri)


@router.get('/twitter/auth')
async def twitter_auth(request: Request):
    token = await oauth.twitter.authorize_access_token(request)
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    resp = await oauth.twitter.get(
        url, params={'skip_status': True, 'include_email': True}, token=token)
    user = resp.json()

    user_data = models.User.check_user_exists(user['email'])
    if user_data:
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['email'])})
    else:
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(user['profile_image_url_https'])
        new_user = models.User.create_user(str(user['id']), user['screen_name'], user['email'], short_url)
        if new_user:
            return JSONResponse({'status_code': 200,
                                 'msg': 'New User Created! Login Successful',
                                 'access_token': create_token(user['email'])})
        else:
            return RedirectResponse(url='/')

