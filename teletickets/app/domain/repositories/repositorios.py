from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.aggregates.venta import Venta
from app.domain.entities.cliente import Cliente
from app.domain.entities.evento import Evento
from app.domain.entities.ticket import Ticket


class Repositorio(ABC):
    """Interfaz genérica de repositorio (patrón colección en memoria)."""

    @abstractmethod
    def get_by_id(self, id_: str): ...

    @abstractmethod
    def get_all(self) -> List: ...

    @abstractmethod
    def save(self, agregado): ...

    @abstractmethod
    def delete(self, id_: str) -> bool: ...


class EventoRepositorio(Repositorio, ABC):
    """Puente entre el Dominio y la Infraestructura para la entidad Evento."""

    @abstractmethod
    def get_by_id(self, evento_id: str) -> Optional[Evento]: ...

    @abstractmethod
    def get_all(self) -> List[Evento]: ...

    @abstractmethod
    def get_activos(self) -> List[Evento]: ...

    @abstractmethod
    def save(self, evento: Evento) -> None: ...

    @abstractmethod
    def delete(self, evento_id: str) -> bool: ...


class ClienteRepositorio(Repositorio, ABC):
    @abstractmethod
    def get_by_id(self, cliente_id: str) -> Optional[Cliente]: ...

    @abstractmethod
    def get_all(self) -> List[Cliente]: ...

    @abstractmethod
    def get_por_email(self, email: str) -> Optional[Cliente]: ...

    @abstractmethod
    def save(self, cliente: Cliente) -> None: ...

    @abstractmethod
    def delete(self, cliente_id: str) -> bool: ...


class VentaRepositorio(Repositorio, ABC):
    """Repositorio del agregado Venta (se persiste como unidad transaccional)."""

    @abstractmethod
    def get_by_id(self, venta_id: str) -> Optional[Venta]: ...

    @abstractmethod
    def get_all(self) -> List[Venta]: ...

    @abstractmethod
    def get_por_cliente(self, cliente_id: str) -> List[Venta]: ...

    @abstractmethod
    def save(self, venta: Venta) -> None: ...

    @abstractmethod
    def delete(self, venta_id: str) -> bool: ...


class TicketRepositorio(Repositorio, ABC):
    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[Ticket]: ...

    @abstractmethod
    def get_all(self) -> List[Ticket]: ...

    @abstractmethod
    def get_por_evento(self, evento_id: str) -> List[Ticket]: ...

    @abstractmethod
    def save(self, ticket: Ticket) -> None: ...

    @abstractmethod
    def delete(self, ticket_id: str) -> bool: ...
