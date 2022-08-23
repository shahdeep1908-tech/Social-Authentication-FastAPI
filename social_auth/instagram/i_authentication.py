from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from social_auth import oauth, models
from starlette.responses import JSONResponse
from social_auth.oauth2 import create_token


router = APIRouter(
    tags=["Authentication"]
)

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
    redirect_uri = request.url_for('insta_auth')
    return await oauth.instagram.authorize_redirect(request, redirect_uri)


@router.get('/instagram/auth')
async def insta_auth(request: Request):
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
