from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
import pyshorteners


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
    print(token)
    url = 'https://api.github.com/user'
    resp = await oauth.github.get(url, token=token)
    user = resp.json()

    user_data = models.User.check_user_exists(user['login'])
    if user_data:
        return {'status_code': 200,
                'msg': 'User Exists! Login Successful',
                'data': user}
    else:
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(user['avatar_url'])
        new_user = models.User.create_user(str(user['id']), user['login'], None, short_url)
        if new_user:
            return {'status_code': 200,
                    'msg': 'New User Created! Login Successful',
                    'data': user}
        else:
            return RedirectResponse(url='/')
