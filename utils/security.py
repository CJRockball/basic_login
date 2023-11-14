from typing import Dict, Optional

from fastapi import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from rich.console import Console
console = Console()

from utils.exception import NotAuthenticatedException

import os
from dotenv import load_dotenv

load_dotenv()

COOKIE_NAME = os.getenv('COOKIE_NAME')



### Authenticate Logic
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )


    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise NotAuthenticatedException
            # HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED,
            #         detail="Not authenticated",
            #         headers={"WWW-Authenticate": "Bearer"},
            #         )
            else:
                return None
        return param