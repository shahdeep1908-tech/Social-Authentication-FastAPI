from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth


config = Config('.env')
oauth = OAuth(config)


def create_app():
    app = FastAPI(
        title='Social Authentication Routes',
        description='GOOGLE | SOCIAL AUTHENTICATION',
        version='1.0.0',
    )
    app.add_middleware(SessionMiddleware, secret_key="!secret")

    from social_auth.google import g_authentication
    from social_auth.twitter import t_authentication
    from social_auth.facebook import f_authentication

    app.include_router(g_authentication.router)
    app.include_router(t_authentication.router)
    app.include_router(f_authentication.router)

    return app