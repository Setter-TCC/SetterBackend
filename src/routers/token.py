from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.internal.validators import token_validator
from src.utils.jwt import generate_payload, generate_token

token_router = APIRouter(prefix="/token")


@token_router.get("/refresh", tags=["Token"])
async def refresh_token(token: dict = Depends(token_validator)):
    username = token.get("sub")
    token_paylaod = generate_payload(username=username)
    token = generate_token(token_paylaod)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "token": {
                "token": token.get("token"),
                "expire": token.get("exp")
            }
        }
    )
