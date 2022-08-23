import json
from starlette.responses import HTMLResponse
from social_auth import models


class SocialAuthHomepage:
    def __init__(self, request, ):
        self.email = None
        self.request = request

    def homepage(self):
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
        self.email = email
        userData = models.User.get_user_data(self.email)
        return userData
