from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth


router = APIRouter(
    tags=["Authentication"]
)

instagram = oauth.register(
    name='instagram',
    access_token_url='https://api.instagram.com/oauth/access_token ',
    authorize_url='https://api.instagram.com/oauth/authorize',
    client_kwargs={'scope': 'user_profile user_media'},
)


@router.get('/instagram/login')
async def login(request: Request):
    redirect_uri = request.url_for('insta_auth')
    return await oauth.instagram.authorize_redirect(request, redirect_uri)


@router.get('/instagram/auth')
async def insta_auth(request: Request):
    token = await oauth.instagram.authorize_access_token(request)
    profile = 'https://graph.instagram.com/v14.0/me'
    resp = await oauth.instagram.get(profile, token=token)
    user = resp.json()
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')
