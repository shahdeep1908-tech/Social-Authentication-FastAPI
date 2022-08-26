from datetime import datetime, timezone
from datetime import timedelta
from config import Settings

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

"""
Generate jwt access_token and verify token function Once user is login with Social Auth token.
jwt token is generated with fastapi OAuth2PasswordBearer.
"""

# Configuration
API_SECRET_KEY = Settings().API_SECRET_KEY
API_ALGORITHM = Settings().API_ALGORITHM
API_ACCESS_TOKEN_EXPIRE_MINUTES = 30

"""
Token url (We should later create a token url that accepts just a user and a password to use swagger)
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Creates jwt access_token with the data passed by login routes.
    :param data: dict - username/email as per data passed from login routes.
    :param expires_delta: time - Specifies time or None.
    :return: encoded jwt which can be used to fetch userdata
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # to_encode.update({'exp': expire})
    to_encode['exp'] = expire
    return jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)


# Create token for an email
def create_token(email):
    """
    Calls create_access_token function to fetch jwt token and pass to auth route
    :param email: str - email fetched from social auth to create jwt token for login user
    :return: str - access_token
    """
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={'sub': email}, expires_delta=access_token_expires)


async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    """
    Decode the encoded jwt token to fetch the actual email to let user login in restricted routes
    :param token: str - access_token
    :return: email if exists or jwtError
    """
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])
        if email := payload.get('sub'):
            return email
    except jwt.PyJWTError as e:
        raise CREDENTIALS_EXCEPTION from e
