from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from app.domain.aggregates.linea_venta import LineaVenta
from app.domain.entities.cliente import Cliente
from app.domain.entities.evento import Evento
from app.domain.entities.ticket import Ticket
from app.domain.exceptions.domain_exceptions import (
    VentaVaciaError,
    VentaYaConfirmadaError,
)
from app.domain.value_objects.cantidad import Cantidad


class EstadoVenta(Enum):
    BORRADOR = "borrador"      # se van agregando tickets
    CONFIRMADA = "confirmada"  # pagada y con tickets emitidos
    CANCELADA = "cancelada"


class Venta:
    """
    Aggregate Root: Venta (equivalente al Pedido/Carrito de la tienda).

    Unidad de consistencia transaccional que agrupa:
      - La entidad Cliente (comprador)
      - Las líneas internas LineaVenta (Evento + Cantidad + precios)

    CUSTODIA DE LA INTEGRIDAD: cualquier cambio (agregar o quitar tickets,
    confirmar la compra) debe pasar obligatoriamente por este objeto raíz.
    La raíz es la única que reduce el stock del evento y emite los tickets.

    Reglas de negocio aplicadas aquí:
      R3: Máximo 10 tickets por línea (lo garantiza el VO Cantidad).
      R4: No vender más tickets que el stock (reducir_stock del Evento).
      R5: El total se calcula siempre desde las líneas, nunca se fija "a mano".
      R6: Una venta confirmada ya no admite modificaciones.
    """

    def __init__(self, cliente: Cliente, venta_id: str | None = None):
        self._venta_id = venta_id or str(uuid.uuid4())
        self._cliente = cliente
        # Colección interna: nadie agrega líneas directamente, solo vía agregar_evento()
        self._lineas: list[LineaVenta] = []
        self._estado = EstadoVenta.BORRADOR
        self._fecha_creacion = datetime.now()
        self._tickets_emitidos: list[Ticket] = []

    # ---- Propiedades de solo lectura ----

    @property
    def venta_id(self) -> str:
        return self._venta_id

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def lineas(self) -> tuple[LineaVenta, ...]:
        """Se expone una COPIA inmutable: el exterior no puede alterar la lista."""
        return tuple(self._lineas)

    @property
    def estado(self) -> EstadoVenta:
        return self._estado

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @property
    def tickets_emitidos(self) -> tuple[Ticket, ...]:
        return tuple(self._tickets_emitidos)

    # ---- Comportamientos del dominio (único punto de acceso) ----

    def _verificar_editable(self) -> None:
        if self._estado != EstadoVenta.BORRADOR:
            raise VentaYaConfirmadaError(self._venta_id)

    def agregar_evento(self, evento: Evento, cantidad: Cantidad) -> None:
        """
        Agrega tickets de un evento a la venta. La raíz valida:
        - R2: el evento debe estar activo (verificar_disponibilidad).
        - No duplicar líneas: si el evento ya está, se aumenta su cantidad.
        """
        self._verificar_editable()
        evento.verificar_disponibilidad()

        for linea in self._lineas:
            if linea.evento == evento:
                linea.aumentar_cantidad(cantidad.valor)
                return

        self._lineas.append(LineaVenta(evento, cantidad))

    def quitar_evento(self, evento: Evento) -> None:
        """Elimina una línea completa de la venta."""
        self._verificar_editable()
        self._lineas = [l for l in self._lineas if l.evento != evento]

    @property
    def total(self):
        """R5: el total se DERIVA de las líneas usando VO Dinero.sumar (inmutable)."""
        from decimal import Decimal
        from app.domain.value_objects.dinero import Dinero

        resultado = Dinero(Decimal("0"))
        for linea in self._lineas:
            resultado = resultado.sumar(linea.subtotal)
        return resultado

    @property
    def total_tickets(self) -> int:
        return sum(l.cantidad.valor for l in self._lineas)

    def confirmar(self) -> list[Ticket]:
        """
        Cierra la transacción:
        - Reduce el stock de cada evento (R4, validado por la entidad Evento).
        - Emite los tickets de la venta.
        - Cambia el estado a CONFIRMADA (R6).
        """
        self._verificar_editable()
        if not self._lineas:
            raise VentaVaciaError()

        for linea in self._lineas:
            # La raíz custodia: reserva el stock a través de la entidad Evento
            linea.evento.reducir_stock(linea.cantidad.valor)
            # Emisión de tickets uno por uno
            for _ in range(linea.cantidad.valor):
                self._tickets_emitidos.append(
                    Ticket(
                        codigo_evento=linea.evento.evento_id,
                        nombre_evento=linea.evento.nombre,
                        nombre_cliente=self._cliente.nombre_completo,
                    )
                )

        self._estado = EstadoVenta.CONFIRMADA
        return list(self._tickets_emitidos)

    def cancelar(self) -> None:
        """Cancela la venta y anula sus tickets emitidos."""
        self._estado = EstadoVenta.CANCELADA
        for ticket in self._tickets_emitidos:
            try:
                ticket.anular()
            except ValueError:
                pass  # tickets ya usados no se anulan

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Venta):
            return False
        return self._venta_id == otro._venta_id

    def __hash__(self) -> int:
        return hash(self._venta_id)

    def __repr__(self) -> str:
        return (
            f"Venta(id='{self._venta_id}', cliente='{self._cliente.nombre_completo}', "
            f"tickets={self.total_tickets}, total={self.total}, estado={self._estado.value})"
        )
