from __future__ import annotations

import uuid
from enum import Enum


class EstadoTicket(Enum):
    """Estados posibles de un ticket emitido."""
    EMITIDO = "emitido"
    VALIDADO = "validado"   # escaneado en el ingreso al evento
    ANULADO = "anulado"     # cancelado antes del evento


class Ticket:
    """
    Entidad: Ticket.

    Representa una entrada individual a un evento. Tiene un código único
    (ticket_id / codigo) que la identifica durante todo su ciclo de vida,
    aunque cambie de estado (emitido -> validado / anulado).
    """

    def __init__(
        self,
        codigo_evento: str,
        nombre_evento: str,
        nombre_cliente: str,
        butaca: str = "general",
        ticket_id: str | None = None,
    ):
        self._ticket_id = ticket_id or str(uuid.uuid4())
        self._codigo = f"TK-{uuid.uuid4().hex[:8].upper()}"
        self._codigo_evento = codigo_evento
        self._nombre_evento = nombre_evento
        self._nombre_cliente = nombre_cliente
        self._butaca = butaca
        self._estado = EstadoTicket.EMITIDO

    # ---- Propiedades ----

    @property
    def ticket_id(self) -> str:
        return self._ticket_id

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def codigo_evento(self) -> str:
        return self._codigo_evento

    @property
    def nombre_evento(self) -> str:
        return self._nombre_evento

    @property
    def nombre_cliente(self) -> str:
        return self._nombre_cliente

    @property
    def butaca(self) -> str:
        return self._butaca

    @property
    def estado(self) -> EstadoTicket:
        return self._estado

    # ---- Comportamientos del dominio ----

    def validar_ingreso(self) -> None:
        """Marca el ticket como usado al ingresar al evento."""
        if self._estado != EstadoTicket.EMITIDO:
            raise ValueError(f"El ticket {self._codigo} no puede validarse (estado: {self._estado.value}).")
        self._estado = EstadoTicket.VALIDADO

    def anular(self) -> None:
        """Anula el ticket (solo si aún no fue usado)."""
        if self._estado == EstadoTicket.VALIDADO:
            raise ValueError("Un ticket ya validado en el ingreso no puede anularse.")
        self._estado = EstadoTicket.ANULADO

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Ticket):
            return False
        return self._ticket_id == otro._ticket_id

    def __hash__(self) -> int:
        return hash(self._ticket_id)

    def __repr__(self) -> str:
        return (
            f"Ticket(codigo='{self._codigo}', evento='{self._nombre_evento}', "
            f"cliente='{self._nombre_cliente}', estado={self._estado.value})"
        )
