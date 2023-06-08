from fastapi import APIRouter, Depends

from src.internal.validators import token_validator

team_router = APIRouter(prefix="/team", dependencies=[Depends(token_validator)])


