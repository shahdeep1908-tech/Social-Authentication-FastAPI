from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth
from dotenv import load_dotenv

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
    if user:
        request.session['user'] = dict(user)
    print("Facebook User ", user)
    return RedirectResponse(url='/')
