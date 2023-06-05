from datetime import datetime, timedelta
from typing import Dict, Union

from jose import jwt

from src.configs.environment import get_environment_variables


def generate_payload(username: str, expire_in: int = 30) -> Dict[str, Union[str, datetime]]:
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

    return {
        "token": access_token,
        "exp": payload["exp"]
    }
