from fastapi import APIRouter, Depends
from starlette.requests import Request
from social_auth import services
from starlette.responses import RedirectResponse, JSONResponse

from social_auth.oauth2 import get_current_user_email

router = APIRouter(
    tags=["Authentication"]
)


@router.get('/')
async def homepage(request: Request):
    service_obj = services.SocialAuthHomepage(request)
    return service_obj.homepage()


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@router.get('/userdata')
def test2(request: Request, current_user: str = Depends(get_current_user_email)):
    service_obj = services.SocialAuthHomepage(request)
    data = service_obj.user_data(current_user)
    return JSONResponse({'status_code': 200, 'message': 'User Profile Fetched Successfully',
                         'data': data})
