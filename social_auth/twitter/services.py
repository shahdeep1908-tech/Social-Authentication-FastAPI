import json
from starlette.responses import HTMLResponse


class Twitter:
    def __init__(self, request, ):
        self.request = request

    def homepage(self):
        user = self.request.session.get('user')
        if user:
            data = json.dumps(user)
            html = (
                f'<pre>{data}</pre>'
                '<a href="/twitter/logout">logout</a>'
            )
            return HTMLResponse(html)
        return HTMLResponse('<a href="/twitter/login">Twitter Login</a>')