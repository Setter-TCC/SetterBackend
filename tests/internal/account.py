import pytest

from src.internal.account import generate_payload_for_account_create
from src.schemas import ContaRequest, AdministradorSchema, TimeSchema, TreinadorSchema


@pytest.mark.parametrize("test_name, payload, expected_result", [
    ("Test if creation without coach works", ContaRequest(
        administrador=AdministradorSchema(nome="sample name", email="same_email@email.com",
                                          cpf="01234567890", rg="0123456",
                                          data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
                                          nome_usuario="sample_username", senha="password"),
        time=TimeSchema(nome="sample team", naipe=1, cnpj="0123456789012", email="email@email.com")),
     (False, False, "sample team", "sample name", "sample_username", None)
     ),
    ("Test if creation with coach as an admin works", ContaRequest(
        administrador=AdministradorSchema(nome="sample name", email="same_email@email.com",
                                          cpf="01234567890", rg="0123456",
                                          data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
                                          nome_usuario="sample_username", senha="password"),
        time=TimeSchema(nome="sample team2", naipe=1, cnpj="0123456789012", email="email@email.com"),
        treinador=TreinadorSchema(nome="sample name", email="same_email@email.com", cpf="01234567890",
                                  rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z",
                                  telefone="01234567899", cref="1234")),
     (True, True, "sample team2", "sample name", "sample_username")
     ),
    ("Test if creation with coach as an admin works", ContaRequest(
        administrador=AdministradorSchema(nome="sample name", email="same_email@email.com",
                                          cpf="01234567890", rg="0123456",
                                          data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
                                          nome_usuario="sample_username", senha="password"),
        time=TimeSchema(nome="sample team3", naipe=1, cnpj="0123456789012", email="email@email.com"),
        treinador=TreinadorSchema(nome="sample name3", email="same_email3@email.com", cpf="11234567890",
                                  rg="1123456", data_nascimento="2003-07-13T17:18:12.340Z",
                                  telefone="11234567899", cref="1234")),
     (True, False, "sample team3", "sample name", "sample_username")
     ),
])
def test_generate_payload_for_account_create(test_name, payload, expected_result):
    print(test_name)
    coach_sent, coach_is_admin, team, admin_person, admin, admin_integration, \
        coach, coach_person, coach_integration = generate_payload_for_account_create(payload)

    assert coach_sent is expected_result[0]
    assert coach_is_admin is expected_result[1]
    assert team.nome is expected_result[2]
    assert admin_person.nome is expected_result[3]
    assert admin.nome_usuario is expected_result[4]
