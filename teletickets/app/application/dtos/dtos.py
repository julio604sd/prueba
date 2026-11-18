"""
DTOs (Data Transfer Objects) de Teletickets.

Dataclasses FROZEN (inmutables) que la capa Aplicacion usa para transferir
informacion hacia la Presentacion SIN exponer las entidades del dominio.
Cada DTO tiene un metodo estatico `de(...)` que mapea Entidad -> DTO.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.entities.cliente import Cliente
from app.domain.entities.evento import Evento


@dataclass(frozen=True)
class EventoDTO:
    evento_id: str
    nombre: str
    categoria: str
    precio: str          # se transfiere como texto: "S/ 80.00"
    disponibles: int

    @staticmethod
    def de(evento: Evento) -> "EventoDTO":
        return EventoDTO(
            evento_id=evento.evento_id,
            nombre=evento.nombre,
            categoria=evento.categoria,
            precio=str(evento.precio_ticket),
            disponibles=evento.disponible,
        )


@dataclass(frozen=True)
class ClienteDTO:
    cliente_id: str
    nombre_completo: str
    email: str

    @staticmethod
    def de(cliente: Cliente) -> "ClienteDTO":
        return ClienteDTO(
            cliente_id=cliente.cliente_id,
            nombre_completo=cliente.nombre_completo,
            email=str(cliente.email),
        )
