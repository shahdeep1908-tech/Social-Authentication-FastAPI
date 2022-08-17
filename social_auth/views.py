from fastapi import APIRouter
from starlette.requests import Request
from social_auth import services
from starlette.responses import RedirectResponse


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
