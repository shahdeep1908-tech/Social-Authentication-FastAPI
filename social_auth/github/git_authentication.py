from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth


router = APIRouter(
    tags=["Authentication"]
)

github = oauth.register(
    name='github',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@router.get('/github/login')
async def login(request: Request):
    redirect_uri = request.url_for('git_auth')
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get('/github/auth')
async def git_auth(request: Request):
    token = await oauth.github.authorize_access_token(request)
    url = 'https://api.github.com/user'
    resp = await oauth.github.get(url, token=token)
    user = resp.json()
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')
