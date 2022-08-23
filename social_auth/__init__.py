from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth


config = Config('.env')
oauth = OAuth(config)


def create_app():
    app = FastAPI(
        title='Social Authentication Routes',
        description='GOOGLE | TWITTER | FACEBOOK | GITHUB | LINKEDIN | INSTAGRAM --- SOCIAL AUTHENTICATION',
        version='1.0.0',
    )
    app.add_middleware(SessionMiddleware, secret_key="!secret")

    from social_auth.google import g_authentication
    from social_auth.twitter import t_authentication
    from social_auth.facebook import f_authentication
    from social_auth.github import git_authentication
    from social_auth.linkedin import l_authentication
    from social_auth.instagram import i_authentication
    from social_auth import views

    app.include_router(views.router)
    app.include_router(g_authentication.router)
    app.include_router(t_authentication.router)
    app.include_router(f_authentication.router)
    app.include_router(git_authentication.router)
    app.include_router(l_authentication.router)
    app.include_router(i_authentication.router)

    return app
