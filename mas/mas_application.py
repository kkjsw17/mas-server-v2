from fastapi.security import OAuth2PasswordBearer

from mas.utils.controller_utils import create_app

app = create_app()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
