from src.schemas.pessoa import PessoaSchema


class AdministradorSchema(PessoaSchema):
    nome_usuario: str
    senha: str
