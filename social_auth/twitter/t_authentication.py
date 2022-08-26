from typing import Any

import pyshorteners
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

"""
Twitter Login Route: It contains 2 routes /login and /auth routes.
/login route redirect homepage to twitter authentication page.
/auth route goes to twitter login page to fetch access token and further user_data.
"""

router = APIRouter(
    tags=["Authentication"]
)

"""Below are twitter registration urls"""
oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)


@router.get('/twitter/login')
async def login(request: Request) -> Any:
    """
    Creates redirect url and pass to twitter_auth function.
    :param request: Request object - Fetch user request token.
    :return: oauth redirect url
    """
    redirect_uri = request.url_for('twitter_auth')
    return await oauth.twitter.authorize_redirect(request, redirect_uri)


@router.get('/twitter/auth')
async def twitter_auth(request: Request):
    """
    Redirect to twitter login page and create access token and fetch userdata.
    :param request: Request object - Fetch user request token.
    :return: Json Object - login-user access_token.
    """
    token = await oauth.twitter.authorize_access_token(request)
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    resp = await oauth.twitter.get(
        url, params={'skip_status': True, 'include_email': True}, token=token)
    user = resp.json()

    if user_data := models.User.check_user_exists(user['email']):
        print(user_data)
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['email'])})

    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(user['profile_image_url_https'])
    if not (new_user := models.User.create_user(str(user['id']), user['screen_name'], user['email'], short_url)):
        print(new_user)
        return RedirectResponse(url='/')

    return JSONResponse({'status_code': 200,
                         'msg': 'New User Created! Login Successful',
                         'access_token': create_token(user['email'])})
