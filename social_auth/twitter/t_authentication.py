from typing import Any

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth


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
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')
