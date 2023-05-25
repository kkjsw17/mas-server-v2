from typing import Annotated

import inject
from fastapi import APIRouter, Depends
from mas.api.auth.service.google_oauth2_service import GoogleOAuth2Service
from mas.api.user.entity.user import User
from mas.api.user.repository.user_repository import UserRepository
from mas.utils.const import COOKIE_AUTHORIZATION_NAME, COOKIE_DOMAIN
from starlette.responses import JSONResponse, RedirectResponse

router = APIRouter(tags=["security"])


google_oauth2_service = inject.instance(GoogleOAuth2Service)
user_repository = inject.instance(UserRepository)


@router.get("/login/google")
async def google_login() -> RedirectResponse:
    """
    Handles the Google OAuth2 login flow. Redirects the user to the Google
    authorization URL to authorize the app and generate an access token.

    Returns:
        RedirectResponse: A redirect response to the Google authorization URL.
    """

    authorization_url = await google_oauth2_service.get_authorization_url()

    return RedirectResponse(url=authorization_url, status_code=302)


@router.get("/login/google/callback")
async def login_google_callback(code: str) -> JSONResponse:
    """
    Callback URL that receives the authorization code from Google and generates
    an encoded JWT token. The token is set as an HTTP-only cookie and returned as
    a JSON response.

    Args:
        code (str): The authorization code received from Google.

    Returns:
        JSONResponse: A JSON response containing the encoded JWT token and token type.
    """

    encoded_jwt_token = await google_oauth2_service.generate_token(code)

    response = JSONResponse({"access_token": encoded_jwt_token, "token_type": "Bearer"})
    response.set_cookie(
        key=COOKIE_AUTHORIZATION_NAME,
        value=f"Bearer {encoded_jwt_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
    )

    return response


@router.get("/logout")
async def logout_and_remove_cookie() -> RedirectResponse:
    """
    Logs the user out by deleting the HTTP-only authorization cookie and redirecting
    the user to the Google logout URL.

    Returns:
        RedirectResponse: A redirect response to the Google logout URL.
    """

    response = RedirectResponse(url=google_oauth2_service.google_auth_flow.redirect_uri)
    response.delete_cookie(COOKIE_AUTHORIZATION_NAME, domain=COOKIE_DOMAIN)

    return response


@router.get("/test")
async def test(
    user: Annotated[User, Depends(google_oauth2_service.get_current_user)]
) -> User:
    """
    Test endpoint that requires an authorized user. Returns the user object
    decoded from the encoded JWT token in the authorization cookie.

    Args:
        user (User): An annotated user object.

    Returns:
        User: The decoded user object.
    """

    return user
