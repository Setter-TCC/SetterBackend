from datetime import datetime, timedelta
from typing import Dict, Union

from fastapi import HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.configs.environment import get_environment_variables
from src.repositories import admin_repository


def generate_payload(username: str, expire_in: int = 120) -> Dict[str, Union[str, datetime]]:
    sub = username
    exp = datetime.utcnow() + timedelta(minutes=expire_in)
    return {
        "sub": sub,
        "exp": exp
    }


def generate_token(payload: Dict[str, Union[str, datetime]]):
    env = get_environment_variables()
    SECRET_KEY = env.SECRET_KEY
    ALGORITHM = env.ALGORITHM

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    payload["exp"] = datetime.utcnow() + timedelta(hours=2)

    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "token": access_token,
        "refresh": refresh_token,
        "exp": payload.get("exp")
    }


def verify_token(access_token, db: Session) -> dict:
    env = get_environment_variables()
    SECRET_KEY = env.SECRET_KEY
    ALGORITHM = env.ALGORITHM

    try:
        data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_on_db = admin_repository.get_admin_by_nome_usuario(db=db, nome_usuario=data.get("sub"))
        if admin_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )

        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )
