from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

"""
Instagram Login Route: It contains 2 routes /login and /auth routes.
/login route redirect homepage to instagram authentication page.
/auth route goes to instagram login page to fetch access token and further user_data.
"""

router = APIRouter(
    tags=["Authentication"]
)

"""Below are instagram registration urls"""
instagram = oauth.register(
        name='instagram',
        api_base_url='https://api.instagram.com',
        access_token_url='https://api.instagram.com/oauth/access_token',
        authorize_url='https://api.instagram.com/oauth/authorize',
        client_kwargs={
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'user_profile user_media'
        },
)


@router.get('/instagram/login')
async def login(request: Request):
    """
    Creates redirect url and pass to insta_auth function.
    :param request: Request object - Fetch user request token.
    :return: oauth redirect url
    """
    redirect_uri = request.url_for('insta_auth')
    return await oauth.instagram.authorize_redirect(request, redirect_uri)


@router.get('/instagram/auth')
async def insta_auth(request: Request):
    """
    Redirect to instagram login page and create access token and fetch userdata.
    :param request: Request object - Fetch user request token.
    :return: Json Object - login-user access_token.
    """
    token = await oauth.instagram.authorize_access_token(request)
    url = 'https://graph.instagram.com/v14.0/me'
    resp = await oauth.instagram.get(url, token=token)
    user_id = resp.json()

    account_url = f'https://graph.instagram.com/{user_id["id"]}?fields=id,account_type,username,media_count'
    acc_resp = await oauth.instagram.get(account_url, token=token)
    user = acc_resp.json()

    user_data = models.User.check_user_exists(user['username'])
    if user_data:
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['username'])})
    else:
        new_user = models.User.create_user(str(user['id']), user['username'], None, None)
        if new_user:
            return JSONResponse({'status_code': 200,
                                 'msg': 'New User Created! Login Successful',
                                 'access_token': create_token(user['username'])})
        else:
            return RedirectResponse(url='/')
