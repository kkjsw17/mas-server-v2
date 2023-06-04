from fastapi import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Get a Bearer-type OAuth2 token stored as a cookie in the request header

    Args:
        tokenUrl (str): The token URL used to obtain the token.
        scheme_name (str): The name of the scheme.
        scopes (dict): The scopes required to access the endpoint.
        auto_error (bool): Whether to automatically raise an HTTPException if the user is not authenticated.
        authorization_name (str): The name of the authorization header.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
        authorization_name: str = "Authorization",
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
        self.authorization_name = authorization_name

    async def __call__(self, request: Request) -> str | None:
        """
        Get the Bearer-type OAuth2 token stored as a cookie in the request header.

        Args:
            request (Request): The request object.

        Returns:
            str | None: The OAuth2 token or None if the user is not authenticated.
        """
        header_authorization = request.headers.get(self.authorization_name)
        cookie_authorization = request.cookies.get(self.authorization_name)

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            _, param = header_scheme, header_param
        elif cookie_scheme.lower() == "bearer":
            _, param = cookie_scheme, cookie_param
        else:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            return None

        return param
