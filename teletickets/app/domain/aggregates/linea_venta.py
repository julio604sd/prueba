from __future__ import annotations

from app.domain.entities.evento import Evento
from app.domain.exceptions.domain_exceptions import StockInsuficienteError
from app.domain.value_objects.cantidad import Cantidad
from app.domain.value_objects.dinero import Dinero


class LineaVenta:
    """
    Componente interno del agregado Venta (similar a ItemPedido en la tienda).

    Tiene identidad LOCAL dentro de la venta: referencia a un Evento,
    una Cantidad (VO) y el precio unitario capturado (VO Dinero).
    No se accede a ella desde fuera: solo a través de la raíz Venta.
    """

    def __init__(self, evento: Evento, cantidad: Cantidad):
        self._evento = evento
        self._cantidad = cantidad
        # Se captura el precio unitario al momento de agregar la línea
        self._precio_unitario = evento.precio_ticket

    @property
    def evento(self) -> Evento:
        return self._evento

    @property
    def cantidad(self) -> Cantidad:
        return self._cantidad

    @property
    def precio_unitario(self) -> Dinero:
        return self._precio_unitario

    @property
    def subtotal(self) -> Dinero:
        """Subtotal = precio unitario x cantidad (operación inmutable del VO)."""
        return self._precio_unitario.multiplicar(self._cantidad.valor)

    def aumentar_cantidad(self, extra: int) -> None:
        """La línea solo puede crecer respetando el stock del evento (R4)."""
        if extra > self._evento.disponible:
            raise StockInsuficienteError(
                self._evento.nombre, extra, self._evento.disponible
            )
        self._cantidad = Cantidad(self._cantidad.valor + extra)

    def __repr__(self) -> str:
        return (
            f"LineaVenta(evento='{self._evento.nombre}', "
            f"cantidad={self._cantidad}, subtotal={self.subtotal})"
        )
