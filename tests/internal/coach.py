import pytest

from src.internal.coach import generate_payload_for_coach_create
from src.schemas import TreinadorRequest


@pytest.mark.parametrize("test_name, payload, expected_result", [
    ("Test sample coach creation", TreinadorRequest(
        nome="random name", email="random_email@email.com", cpf="01234567890",
        rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
        cref="1234", time_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        data_inicio="2023-07-13T17:18:12.340Z"),
     ("random name", "random_email@email.com", "01234567890", "1234")),
    ("Test sample coach creation 2", TreinadorRequest(
        nome="foo bar", email="foo_bar@email.com", cpf="11223344556",
        rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
        cref="5555", time_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        data_inicio="2023-07-13T17:18:12.340Z"),
     ("foo bar", "foo_bar@email.com", "11223344556", "5555")),
    ("Test sample coach creation 3", TreinadorRequest(
        nome="lorem ipsum", email="loremipsum@email.com", cpf="00998877665",
        rg="0123456", data_nascimento="2023-07-13T17:18:12.340Z", telefone="01234567899",
        cref="9876", time_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        data_inicio="2023-07-13T17:18:12.340Z"),
     ("lorem ipsum", "loremipsum@email.com", "00998877665", "9876")),
])
def test_generate_payload_for_account_create(test_name, payload, expected_result):
    print(test_name)
    tecnico, integracao, pessoa_tecnico = generate_payload_for_coach_create(payload)

    assert pessoa_tecnico.nome == expected_result[0]
    assert pessoa_tecnico.email == expected_result[1]
    assert pessoa_tecnico.cpf == expected_result[2]
    assert tecnico.cref == expected_result[3]
    assert integracao.time_id == payload.time_id
    assert integracao.pessoa_id == tecnico.id
    assert tecnico.id == pessoa_tecnico.id
