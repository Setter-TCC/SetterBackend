from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.validators import token_validator, validate_user_authorization
from src.repositories import time_repository
from src.schemas import TimeSchema

team_router = APIRouter(prefix="/team", dependencies=[Depends(token_validator)])


@team_router.get("", tags=["Time"])
async def get_team_data(team_id: UUID, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)
    team = time_repository.get_time_by_id(db=db, time_id=team_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching team.",
            "value": {
                "id": str(team.id),
                "nome": team.nome,
                "email": team.email,
                "naipe": team.naipe.value,
                "cnpj": team.cnpj
            }
        }
    )


@team_router.put("/update", tags=["Time"])
async def update_team(request: TimeSchema, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    if not request.id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request body is not well formated."
        )

    await validate_user_authorization(db, request.id, token)

    time_ok = time_repository.update_time(db=db, time=request)
    if not time_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Team could not be updated."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Updated team succesfully."
        }
    )
