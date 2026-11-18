"""
Implementaciones concretas de los Repositorios del Dominio.

Cada repositorio implementa la interfaz abstracta definida en
app/domain/repositories y guarda los objetos en la BaseDeDatosSimulada.
"""

from typing import List, Optional

from app.domain.aggregates.venta import Venta
from app.domain.entities.cliente import Cliente
from app.domain.entities.evento import Evento
from app.domain.entities.ticket import Ticket
from app.domain.repositories.repositorios import (
    ClienteRepositorio,
    EventoRepositorio,
    TicketRepositorio,
    VentaRepositorio,
)
from app.infrastructure.base_datos import BaseDeDatosSimulada


class EventoRepositorioMemoria(EventoRepositorio):
    def __init__(self, db: BaseDeDatosSimulada):
        self._db = db

    def get_by_id(self, evento_id: str) -> Optional[Evento]:
        return self._db.eventos.get(evento_id)

    def get_all(self) -> List[Evento]:
        return list(self._db.eventos.values())

    def get_activos(self) -> List[Evento]:
        return [e for e in self._db.eventos.values() if e.activo]

    def save(self, evento: Evento) -> None:
        self._db.eventos[evento.evento_id] = evento

    def delete(self, evento_id: str) -> bool:
        return self._db.eventos.pop(evento_id, None) is not None


class ClienteRepositorioMemoria(ClienteRepositorio):
    def __init__(self, db: BaseDeDatosSimulada):
        self._db = db

    def get_by_id(self, cliente_id: str) -> Optional[Cliente]:
        return self._db.clientes.get(cliente_id)

    def get_all(self) -> List[Cliente]:
        return list(self._db.clientes.values())

    def get_por_email(self, email: str) -> Optional[Cliente]:
        email_normalizado = email.strip().lower()
        for c in self._db.clientes.values():
            if c.email.direccion == email_normalizado:
                return c
        return None

    def save(self, cliente: Cliente) -> None:
        self._db.clientes[cliente.cliente_id] = cliente

    def delete(self, cliente_id: str) -> bool:
        return self._db.clientes.pop(cliente_id, None) is not None


class VentaRepositorioMemoria(VentaRepositorio):
    def __init__(self, db: BaseDeDatosSimulada):
        self._db = db

    def get_by_id(self, venta_id: str) -> Optional[Venta]:
        return self._db.ventas.get(venta_id)

    def get_all(self) -> List[Venta]:
        return list(self._db.ventas.values())

    def get_por_cliente(self, cliente_id: str) -> List[Venta]:
        return [v for v in self._db.ventas.values() if v.cliente.cliente_id == cliente_id]

    def save(self, venta: Venta) -> None:
        # El agregado Venta se persiste COMPLETO como unidad transaccional
        self._db.ventas[venta.venta_id] = venta

    def delete(self, venta_id: str) -> bool:
        return self._db.ventas.pop(venta_id, None) is not None


class TicketRepositorioMemoria(TicketRepositorio):
    def __init__(self, db: BaseDeDatosSimulada):
        self._db = db

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        return self._db.tickets.get(ticket_id)

    def get_all(self) -> List[Ticket]:
        return list(self._db.tickets.values())

    def get_por_evento(self, evento_id: str) -> List[Ticket]:
        return [t for t in self._db.tickets.values() if t.codigo_evento == evento_id]

    def save(self, ticket: Ticket) -> None:
        self._db.tickets[ticket.ticket_id] = ticket

    def delete(self, ticket_id: str) -> bool:
        return self._db.tickets.pop(ticket_id, None) is not None
