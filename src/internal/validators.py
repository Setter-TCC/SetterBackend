from uuid import UUID

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.repositories import admin_repository, integracao_repository
from src.utils.enums import TipoPessoa
from src.utils.jwt import verify_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/account/login")


async def validate_user_authorization(db: Session, time_id: UUID, token: dict):
    username = token.get("sub")
    user_on_db = admin_repository.get_admin_by_nome_usuario(db=db, nome_usuario=username)

    if not user_on_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    integracao_on_db = integracao_repository.get_integracao_by_user_and_team_id(db=db, user_id=user_on_db.id,
                                                                                team_ID=time_id)
    if not integracao_on_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not allowed to modify this team."
        )

    if not integracao_on_db.ativo or integracao_on_db.tipo_pessoa != TipoPessoa.administrador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not allowed to modify this team."
        )


def token_validator(db: Session = Depends(get_db), token=Depends(oauth_scheme)) -> dict:
    data = verify_token(token, db)
    return data
