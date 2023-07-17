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

    integracao_on_db = integracao_repository.get_admin_integracao_by_user_and_team_id(db=db, user_id=user_on_db.id,
                                                                                      team_id=time_id)
    if not integracao_on_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not allowed to modify this team because it was not found."
        )

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(f"IntegracaoIntegra")
    print(f"ativo:       {integracao_on_db.ativo}")
    print(f"tipo pessoa: {integracao_on_db.tipo_pessoa.name}")
    print(f"time_id:     {str(integracao_on_db.time_id)}")
    print(f"pessoa_id:   {str(integracao_on_db.pessoa_id)}")
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    if not integracao_on_db.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not allowed to modify this team becausa it is not active. aaaaaaaaaaaa"
        )

    if not integracao_on_db.ativo or integracao_on_db.tipo_pessoa != TipoPessoa.administrador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not allowed to modify this team becausa it is not an admin. He is {integracao_on_db.tipo_pessoa.name}"
        )


def token_validator(db: Session = Depends(get_db), token=Depends(oauth_scheme)) -> dict:
    data = verify_token(token, db)
    return data
