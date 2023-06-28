from src.utils.enums import TipoTransacao


def get_transaction_origin(team_name: str, transaction_name: str, person_name: str,
                           tipo_transacao: TipoTransacao) -> str:
    if tipo_transacao == TipoTransacao.despesa or tipo_transacao == TipoTransacao.tecnico:
        return team_name

    elif tipo_transacao == TipoTransacao.ganho:
        return transaction_name

    elif tipo_transacao == TipoTransacao.mensalidade:
        return person_name

    else:
        return ""


def get_transaction_destiny(team_name: str, transaction_name: str, person_name: str,
                            tipo_transacao: TipoTransacao) -> str:
    if tipo_transacao == TipoTransacao.ganho or tipo_transacao == TipoTransacao.mensalidade:
        return team_name

    elif tipo_transacao == TipoTransacao.tecnico:
        return person_name

    elif tipo_transacao == TipoTransacao.despesa:
        return transaction_name

    else:
        return ""
