import pyshorteners
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token

"""
LinkedIn Login Route: It contains 2 routes /login and /auth routes.
/login route redirect homepage to linkedin authentication page.
/auth route goes to linkedin login page to fetch access token and further user_data.
"""

router = APIRouter(
    tags=["Authentication"]
)

"""Below are linkedin registration urls"""
linkedin = oauth.register(
    name='linkedin',
    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
    client_kwargs={'scope': 'r_liteprofile r_emailaddress'},
)


@router.get('/linkedin/login')
async def login(request: Request):
    """
    Creates redirect url and pass to linkedin_auth function.
    :param request: Request object - Fetch user request token.
    :return: oauth redirect url
    """
    redirect_uri = request.url_for('linkedin_auth')
    return await oauth.linkedin.authorize_redirect(request, redirect_uri)


@router.get('/linkedin/auth')
async def linkedin_auth(request: Request):
    """
    Redirect to linkedin login page and create access token and fetch userdata.
    :param request: Request object - Fetch user request token.
    :return: Json Object - login-user access_token.
    """
    token = await oauth.linkedin.authorize_access_token(request)
    profile = 'https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))'
    prof_resp = await oauth.linkedin.get(profile, token=token)
    user = prof_resp.json()
    email = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
    resp = await oauth.linkedin.get(email, token=token)
    email = resp.json()
    user['EmailAddress'] = email

    user_data = models.User.check_user_exists(user['EmailAddress']['elements'][0]['handle~']['emailAddress'])
    if user_data:
        return JSONResponse({'status_code': 200,
                             'msg': 'User Exists! Login Successful',
                             'access_token': create_token(user['EmailAddress']['elements'][0]['handle~']['emailAddress'])})
    else:
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(user['profilePicture']['displayImage~']['elements'][0]['identifiers'][0]['identifier'])
        new_user = models.User.create_user(str(user['id']), None, user['EmailAddress']['elements'][0]['handle~']['emailAddress'], short_url)
        if new_user:
            return JSONResponse({'status_code': 200,
                                 'msg': 'New User Created! Login Successful',
                                 'access_token': create_token(user['EmailAddress']['elements'][0]['handle~']['emailAddress'])})
        else:
            return RedirectResponse(url='/')

