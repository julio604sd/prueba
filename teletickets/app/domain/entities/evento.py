from __future__ import annotations

import uuid
from datetime import datetime

from app.domain.exceptions.domain_exceptions import EventoNoDisponibleError, StockInsuficienteError
from app.domain.value_objects.dinero import Dinero


class Evento:
    """
    Entidad: Evento (equivalente al "Producto" de la tienda en línea).

    Es el Aggregate Root del agregado Evento. Gestiona su propio ciclo de
    vida (activo/inactivo), su precio (VO Dinero) y su stock de tickets.

    Reglas de negocio:
      R1: El precio no puede ser negativo (lo garantiza el VO Dinero).
      R2: Solo se venden tickets de eventos activos.
      R4: No se pueden vender más tickets que la capacidad disponible.
    """

    def __init__(
        self,
        nombre: str,
        categoria: str,
        fecha_inicio: datetime,
        precio_ticket: Dinero,
        capacidad_total: int,
        evento_id: str | None = None,
    ):
        self._evento_id = evento_id or str(uuid.uuid4())
        self._nombre = nombre.strip()
        self._categoria = categoria.strip()
        self._fecha_inicio = fecha_inicio
        # VO Dinero: valida precio no negativo (R1)
        self._precio_ticket = precio_ticket
        self._capacidad_total = capacidad_total
        self._tickets_vendidos = 0
        # Por defecto, el evento está activo
        self._activo = True

    # ---- Propiedades de solo lectura ----

    @property
    def evento_id(self) -> str:
        return self._evento_id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def fecha_inicio(self) -> datetime:
        return self._fecha_inicio

    @property
    def precio_ticket(self) -> Dinero:
        return self._precio_ticket

    @property
    def capacidad_total(self) -> int:
        return self._capacidad_total

    @property
    def tickets_vendidos(self) -> int:
        return self._tickets_vendidos

    @property
    def disponible(self) -> int:
        """Tickets aún disponibles para la venta."""
        return self._capacidad_total - self._tickets_vendidos

    @property
    def activo(self) -> bool:
        return self._activo

    # ---- Comportamientos del dominio ----

    def actualizar_precio(self, nuevo_precio: Dinero) -> None:
        """Permite cambiar el precio del ticket. VO Dinero valida R1."""
        self._precio_ticket = nuevo_precio

    def activar(self) -> None:
        """Marca el evento como disponible para la venta."""
        self._activo = True

    def desactivar(self) -> None:
        """Marca el evento como no disponible (R2)."""
        self._activo = False

    def verificar_disponibilidad(self) -> None:
        """Verifica que el evento pueda ser vendido (R2)."""
        if not self._activo:
            raise EventoNoDisponibleError(self._nombre)

    def reducir_stock(self, cantidad: int) -> None:
        """
        Reserva tickets tras una compra. Valida R4 (stock suficiente).
        La verificación de que el evento esté activo (R2) también es
        responsabilidad de esta entidad raíz.
        """
        self.verificar_disponibilidad()
        if cantidad > self.disponible:
            raise StockInsuficienteError(self._nombre, cantidad, self.disponible)
        self._tickets_vendidos += cantidad

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Evento):
            return False
        return self._evento_id == otro._evento_id

    def __hash__(self) -> int:
        return hash(self._evento_id)

    def __repr__(self) -> str:
        return (
            f"Evento(id='{self._evento_id}', nombre='{self._nombre}', "
            f"precio={self._precio_ticket}, disponibles={self.disponible}, "
            f"activo={self._activo})"
        )
