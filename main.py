from social_auth import create_app
from social_auth import models
from database import engine

models.Base.metadata.create_all(engine)

app = create_app()
