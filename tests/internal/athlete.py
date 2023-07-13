import pytest

from src.internal.athlete import generate_payload_for_athlete_create
from src.schemas import AtletaRequest
from src.utils.enums import PosicaoAtleta


@pytest.mark.parametrize("test_name, payload, expected_result", [
    ("Test sample athlete creation", AtletaRequest(
        nome="sample name", email="same_email@email.com", cpf="01234567890",
        rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
        posicao=3, time_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ), ("sample name", "same_email@email.com", "01234567890", PosicaoAtleta(3).value)),
    ("Test sample athlete creation 2", AtletaRequest(
        nome="foo bar", email="foo_bar@email.com", cpf="44455566677",
        rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
        posicao=5, time_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ), ("foo bar", "foo_bar@email.com", "44455566677", PosicaoAtleta(5).value)),
    ("Test sample athlete creation 3", AtletaRequest(
        nome="Random Name", email="random_name@email.com", cpf="99988833322",
        rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
        posicao=1, time_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ), ("Random Name", "random_name@email.com", "99988833322", PosicaoAtleta(1).value)),
])
def test_generate_payload_for_account_create(test_name, payload, expected_result):
    print(test_name)
    atleta, integracao, pessoa_atleta = generate_payload_for_athlete_create(payload)

    assert pessoa_atleta.nome == expected_result[0]
    assert pessoa_atleta.email == expected_result[1]
    assert pessoa_atleta.cpf == expected_result[2]
    assert atleta.posicao == expected_result[3]
    assert atleta.id == pessoa_atleta.id
    assert integracao.time_id == payload.time_id
