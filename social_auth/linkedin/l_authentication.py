from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth


router = APIRouter(
    tags=["Authentication"]
)

linkedin = oauth.register(
    name='linkedin',
    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
    client_kwargs={'scope': 'r_liteprofile r_emailaddress'},
)


@router.get('/linkedin/login')
async def login(request: Request):
    redirect_uri = request.url_for('linkedin_auth')
    return await oauth.linkedin.authorize_redirect(request, redirect_uri)


@router.get('/linkedin/auth')
async def linkedin_auth(request: Request):
    token = await oauth.linkedin.authorize_access_token(request)
    profile = 'https://api.linkedin.com/v2/me'
    resp = await oauth.linkedin.get(profile, token=token)
    user = resp.json()
    email = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
    resp = await oauth.linkedin.get(email, token=token)
    email = resp.json()
    user['EmailAddress'] = email
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')
