from typing import Optional

from src.schemas.pessoa import PessoaSchema


class TreinadorSchema(PessoaSchema):
    cref: Optional[str]
