from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.utils.jwt import generate_payload, generate_token, verify_token

token_router = APIRouter(prefix="/token")


@token_router.get("/refresh", tags=["Token"])
async def refresh_token(token, db: Session = Depends(get_db)):
    token_data = verify_token(token, db=db)
    username = token_data.get("sub")
    token_paylaod = generate_payload(username=username)
    _token = generate_token(token_paylaod)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "token": {
                "token": _token.get("token"),
                "refresh": _token.get("refresh"),
                "expire": _token.get("exp")
            }
        }
    )
