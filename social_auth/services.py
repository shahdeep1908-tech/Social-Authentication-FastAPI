import json
from starlette.responses import HTMLResponse
from social_auth import models

"""
Contains class that handles function for login and logout routes.
This is for UI based view for all social auth functions.
"""


class SocialAuthHomepage:
    def __init__(self, request, ):
        """
        Constructor call while object is created.
        :param request: Request Object - Requested data
        """
        self.email = None
        self.request = request

    def homepage(self):
        """
        HTML Response script for UI based api call
        :return: Social Auth Buttons to redirect on its login routes.
        """
        user = self.request.session.get('user')
        if user:
            data = json.dumps(user)
            html = (
                f'<pre>{data}</pre>'
                '<a href="/logout">logout</a>'
            )
            return HTMLResponse(html)
        return HTMLResponse('<a href="/google/login">Google Login</a>'
                            '<br><hr>'
                            '<a href="/twitter/login">Twitter Login</a>'
                            '<br><hr>'
                            '<a href="/facebook/login">Facebook Login</a>'
                            '<br><hr>'
                            '<a href="/github/login">Github Login</a>'
                            '<br><hr>'
                            '<a href="/linkedin/login">LinkedIn Login</a>'
                            '<br><hr>'
                            '<a href="/instagram/login">Instagram Login</a>')

    def user_data(self, email):
        """
        Fetch userdata from models classmethod once user is verified by access_token
        :param email: str - current_user email
        :return: userData from users Table.
        """
        self.email = email
        userData = models.User.get_user_data(self.email)
        return userData
