from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth
from dotenv import load_dotenv
from social_auth import models
import pyshorteners
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

"""
Facebook Login Route: It contains 2 routes /login and /auth routes.
/login route redirect homepage to facebook authentication page.
/auth route goes to facebook login page to fetch access token and further user_data.
"""

load_dotenv()

router = APIRouter(
    tags=["Authentication"]
)

"""Below are facebook registration urls"""
oauth.register(
    name='facebook',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    api_base_url='https://graph.facebook.com/',
    client_kwargs={'scope': 'email'},
)


@router.get('/facebook/login')
async def login(request: Request):
    """
    Creates redirect url and pass to facebook_auth function.
    :param request: Request object - Fetch user request token.
    :return: oauth redirect url
    """
    redirect_uri = request.url_for('facebook_auth')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


@router.get('/facebook/auth')
async def facebook_auth(request: Request):
    """
    Redirect to facebook login page and create access token and fetch userdata.
    :param request: Request object - Fetch user request token.
    :return: Json Object - login-user access_token.
    """
    token = await oauth.facebook.authorize_access_token(request)
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    print(token)
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    url = 'https://graph.facebook.com/me?fields=id,name,email,picture{url}'
    resp = await oauth.facebook.get(url, token=token)
    user = resp.json()

    if user_data := models.User.check_user_exists(user['email']):
        print(user_data)
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['email'])})

    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(user['picture']['data']['url'])
    if not (new_user := models.User.create_user(user['id'], user['name'], user['email'], short_url)):
        return RedirectResponse(url='/')

    print(new_user)
    return JSONResponse({'status_code': 200,
                         'msg': 'New User Created! Login Successful',
                         'access_token': create_token(user['email'])})
