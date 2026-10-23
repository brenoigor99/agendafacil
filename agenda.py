"""
Módulo principal do sistema AgendaFácil.
Gerencia o agendamento, remarcação e listagem de atendimentos de uma clínica.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

# Constantes de Negócio (Substituem valores mágicos)
HORARIO_MIN_INICIO = 8
HORARIO_MAX_FIM = 18
DURACAO_MIN = 15
DURACAO_MAX = 120
DURACAO_PASSO = 15
STATUS_MARCADO = "MARCADO"


class AgendaError(Exception):
    """Exceção base para erros de negócio no AgendaFácil."""
    pass


class HorarioOcupadoError(AgendaError):
    """Lançada quando o horário solicitado já está ocupado por outro atendimento."""
    pass


class HorarioInvalidoError(AgendaError):
    """Lançada quando o horário ou duração violam as regras do expediente."""
    pass


class DataInvalidaError(AgendaError):
    """Lançada quando o formato da data é inválido."""
    pass


@dataclass
class Atendimento:
    """Representa um atendimento agendado na clínica."""
    paciente: str
    profissional: str
    data: str
    hora: int
    duracao: int
    status: str = STATUS_MARCADO


# Repositório em memória
_agenda: List[Atendimento] = []


def validar_formato_data(data_str: str) -> None:
    """
    Valida se a data está no formato AAAA-MM-DD.

    Args:
        data_str (str): String representando a data.

    Raises:
        DataInvalidaError: Se o formato estiver incorreto.
    """
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError as e:
        raise DataInvalidaError(f"Data inválida ('{data_str}'). O formato deve ser AAAA-MM-DD.") from e


def validar_regras_horario(hora: int, duracao: int) -> None:
    """
    Valida se a hora de início e a duração respeitam o expediente e as regras de negócio.

    Args:
        hora (int): Hora de início do atendimento (8 a 17).
        duracao (int): Duração em minutos (15 a 120, múltiplos de 15).

    Raises:
        HorarioInvalidoError: Se a hora ou duração forem inválidas.
    """
    if not (HORARIO_MIN_INICIO <= hora < HORARIO_MAX_FIM):
        raise HorarioInvalidoError(
            f"Hora de início inválida ({hora}h). O expediente funciona das {HORARIO_MIN_INICIO}h às {HORARIO_MAX_FIM}h."
        )
    if not (DURACAO_MIN <= duracao <= DURACAO_MAX) or (duracao % DURACAO_PASSO != 0):
        raise HorarioInvalidoError(
            f"Duração inválida ({duracao} min). Deve ser entre {DURACAO_MIN} e {DURACAO_MAX} minutos, em múltiplos de {DURACAO_PASSO}."
        )
    
    # Decisão de projeto: O término do atendimento não pode ultrapassar o fim do expediente (18h)
    hora_fim_atendimento = hora + (duracao / 60)
    if hora_fim_atendimento > HORARIO_MAX_FIM:
        raise HorarioInvalidoError(
            f"Atendimento excede o horário de encerramento do expediente ({HORARIO_MAX_FIM}h)."
        )


def existe_conflito(profissional: str, data: str, hora: int) -> bool:
    """
    Verifica se já existe atendimento para o profissional na mesma data e horário.

    Args:
        profissional (str): Nome do profissional.
        data (str): Data no formato AAAA-MM-DD.
        hora (int): Hora do atendimento.

    Returns:
        bool: True se houver conflito, False caso contrário.
    """
    for atendimento in _agenda:
        if atendimento.profissional == profissional and atendimento.data == data and atendimento.hora == hora:
            return True
    return False


def adicionar_atendimento(paciente: str, profissional: str, data: str, hora: int, duracao: int) -> None:
    """
    Adiciona um novo atendimento à agenda após validar todas as pré-condições.

    Args:
        paciente (str): Nome do paciente.
        profissional (str): Nome do profissional.
        data (str): Data no formato AAAA-MM-DD.
        hora (int): Hora de início.
        duracao (int): Duração em minutos.

    Raises:
        DataInvalidaError: Se a data for inválida.
        HorarioInvalidoError: Se o horário/duração forem inválidos.
    """
    if not paciente or not profissional:
        raise ValueError("Nome do paciente e do profissional não podem ser vazios.")

    validar_formato_data(data)
    validar_regras_horario(hora, duracao)

    if existe_conflito(profissional, data, hora):
        print("Horario ocupado")
        return

    novo_atendimento = Atendimento(
        paciente=paciente,
        profissional=profissional,
        data=data,
        hora=hora,
        duracao=duracao
    )
    _agenda.append(novo_atendimento)
    print("Atendimento marcado para", paciente)


def remarcar_atendimento(paciente: str, data_atual: str, hora_atual: int, nova_data: str, nova_hora: int) -> None:
    """
    Remarca um atendimento existente para uma nova data e horário.

    Args:
        paciente (str): Nome do paciente.
        data_atual (str): Data atual do atendimento.
        hora_atual (int): Hora atual do atendimento.
        nova_data (str): Nova data no formato AAAA-MM-DD.
        nova_hora (int): Nova hora de início.

    Raises:
        DataInvalidaError: Se alguma das datas for inválida.
        HorarioInvalidoError: Se a nova hora for inválida.
    """
    validar_formato_data(data_atual)
    validar_formato_data(nova_data)
    
    atendimento_alvo = None
    for atendimento in _agenda:
        if atendimento.paciente == paciente and atendimento.data == data_atual and atendimento.hora == hora_atual:
            atendimento_alvo = atendimento
            break

    if not atendimento_alvo:
        raise ValueError(f"Atendimento não encontrado para {paciente} em {data_atual} às {hora_atual}h.")

    validar_regras_horario(nova_hora, atendimento_alvo.duracao)

    if existe_conflito(atendimento_alvo.profissional, nova_data, nova_hora):
        print("Horario ocupado")
        return

    atendimento_alvo.data = nova_data
    atendimento_alvo.hora = nova_hora
    print("Remarcado")


def listar_atendimentos_por_data(data: str) -> None:
    """
    Lista todos os atendimentos agendados para uma determinada data.

    Args:
        data (str): Data no formato AAAA-MM-DD.

    Raises:
        DataInvalidaError: Se a data for inválida.
    """
    validar_formato_data(data)
    for atendimento in _agenda:
        if atendimento.data == data:
            print(atendimento.hora, atendimento.paciente, atendimento.profissional, atendimento.status)


if __name__ == "__main__":
    # Programa de demonstração exigido
    adicionar_atendimento("Ana", "Dr. Silva", "2026-10-05", 9, 30)
    adicionar_atendimento("Bruno", "Dr. Silva", "2026-10-05", 9, 30)
    adicionar_atendimento("Carla", "Dra. Souza", "2026-10-05", 14, 60)
    remarcar_atendimento("Ana", "2026-10-05", 9, "2026-10-06", 10)
    listar_atendimentos_por_data("2026-10-05")