import pytest

from src.internal.transaction import get_transaction_destiny, get_transaction_origin
from src.utils.enums import TipoTransacao


@pytest.mark.parametrize("test_name, team_name, transaction_name, person_name, tipo_transacao, expected_result", [
    ("Test mensality destiny", "team_name", "transaction_name", "person_name", TipoTransacao.mensalidade,
     "team_name"),
    ("Test coach destiny", "team_name", "transaction_name", "person_name", TipoTransacao.tecnico, "person_name"),
    ("Test incoming destiny", "team_name", "transaction_name", "person_name", TipoTransacao.despesa, "transaction_name"),
    ("Test earn destiny", "team_name", "transaction_name", "person_name", TipoTransacao.ganho, "team_name"),
])
def test_transaction_destiny(test_name, team_name, transaction_name, person_name, tipo_transacao, expected_result):
    result = get_transaction_destiny(team_name, transaction_name, person_name, tipo_transacao)
    assert result == expected_result

@pytest.mark.parametrize("test_name, team_name, transaction_name, person_name, tipo_transacao, expected_result", [
    ("Test mensality destiny", "team_name", "transaction_name", "person_name", TipoTransacao.mensalidade,
     "person_name"),
    ("Test coach destiny", "team_name", "transaction_name", "person_name", TipoTransacao.tecnico, "team_name"),
    ("Test incoming destiny", "team_name", "transaction_name", "person_name", TipoTransacao.despesa, "team_name"),
    ("Test earn destiny", "team_name", "transaction_name", "person_name", TipoTransacao.ganho, "transaction_name"),
])
def test_transaction_origin(test_name, team_name, transaction_name, person_name, tipo_transacao, expected_result):
    result = get_transaction_origin(team_name, transaction_name, person_name, tipo_transacao)
    assert result == expected_result
