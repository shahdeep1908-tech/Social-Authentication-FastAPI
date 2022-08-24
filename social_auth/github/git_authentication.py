from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
import pyshorteners
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

"""
Github Login Route: It contains 2 routes /login and /auth routes.
/login route redirect homepage to github authentication page.
/auth route goes to github login page to fetch access token and further user_data.
"""

router = APIRouter(
    tags=["Authentication"]
)

"""Below are github registration urls"""
github = oauth.register(
    name='github',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@router.get('/github/login')
async def login(request: Request):
    """
    Creates redirect url and pass to git_auth function.
    :param request: Request object - Fetch user request token.
    :return: oauth redirect url
    """
    redirect_uri = request.url_for('git_auth')
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get('/github/auth')
async def git_auth(request: Request):
    """
    Redirect to github login page and create access token and fetch userdata.
    :param request: Request object - Fetch user request token.
    :return: Json Object - login-user access_token.
    """
    token = await oauth.github.authorize_access_token(request)
    print(token)
    url = 'https://api.github.com/user'
    resp = await oauth.github.get(url, token=token)
    user = resp.json()

    user_data = models.User.check_user_exists(user['login'])
    if user_data:
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['login'])})
    else:
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(user['avatar_url'])
        new_user = models.User.create_user(str(user['id']), user['login'], None, short_url)
        if new_user:
            return JSONResponse({'status_code': 200,
                                 'msg': 'New User Created! Login Successful',
                                 'access_token': create_token(user['login'])})
        else:
            return RedirectResponse(url='/')
