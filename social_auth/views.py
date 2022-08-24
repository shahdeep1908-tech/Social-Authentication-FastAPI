from fastapi import APIRouter, Depends
from starlette.requests import Request
from social_auth import services
from starlette.responses import RedirectResponse

from social_auth.oauth2 import get_current_user_email

"""
Common file for API calls for HomePage | Logout | UserData.
Redirect to particular Social Auth Routes Through HTML Response buttons via UI. [If Required].
"""

router = APIRouter(
    tags=["Authentication"]
)


@router.get('/')
async def homepage(request: Request):
    """
    Displays HTML UI based buttons of different social Sites
    :param request: Request Object
    :return: HTML Response Buttons
    """
    service_obj = services.SocialAuthHomepage(request)
    return service_obj.homepage()


@router.get('/logout')
async def logout(request: Request):
    """
    Session logout route is called to finish user session
    :param request: Request Object
    :return: None and redirect to Homepage API
    """
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@router.get('/userdata')
def userdata(request: Request, current_user: str = Depends(get_current_user_email)):
    """
    Fetch User Data from database once token is verified
    :param request: Request Object
    :param current_user: Verified Access_token from Header
    :return: Json Response UserData
    """
    service_obj = services.SocialAuthHomepage(request)
    data = service_obj.user_data(current_user)
    return {'status_code': 200, 'message': 'User Profile Fetched Successfully',
            'data': data}
