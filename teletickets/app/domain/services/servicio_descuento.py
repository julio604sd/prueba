from __future__ import annotations

from decimal import Decimal

from app.domain.aggregates.venta import Venta
from app.domain.entities.cliente import Cliente
from app.domain.value_objects.dinero import Dinero


class ServicioDescuento:
    """
    Domain Service: ServicioDescuento.

    Lógica de negocio que involucra MÚLTIPLES entidades/objetos (Cliente +
    Venta + Dinero) y por tanto NO pertenece naturalmente a una sola clase.

    Reglas de descuento de Teletickets:
      D1: Compra desde 5 tickets -> 10% de descuento.
      D2: Clientes VIP           -> 15% adicional acumulable.
    El servicio devuelve un NUEVO Dinero con el total descontado
    (no muta la venta, respetando la inmutabilidad de los VOs).
    """

    UMBRAL_DESCUENTO_VOLUMEN = 5
    PCT_DESCUENTO_VOLUMEN = Decimal("0.10")
    PCT_DESCUENTO_VIP = Decimal("0.15")

    @staticmethod
    def es_cliente_vip(cliente: Cliente) -> bool:
        """Regla simple de ejemplo: correos del dominio @vip.teletickets.pe."""
        return cliente.email.direccion.endswith("@vip.teletickets.pe")

    def calcular_descuento(self, venta: Venta) -> Dinero:
        """Retorna el monto del descuento aplicable a la venta (puede ser 0)."""
        total = venta.total
        pct = Decimal("0")

        # D1: descuento por volumen
        if venta.total_tickets >= self.UMBRAL_DESCUENTO_VOLUMEN:
            pct += self.PCT_DESCUENTO_VOLUMEN

        # D2: descuento VIP
        if self.es_cliente_vip(venta.cliente):
            pct += self.PCT_DESCUENTO_VIP

        monto = (total.monto * pct).quantize(Decimal("0.01"))
        return Dinero(monto, total.moneda)

    def aplicar_descuento(self, venta: Venta) -> Dinero:
        """Retorna un NUEVO Dinero: total de la venta menos el descuento."""
        total = venta.total
        descuento = self.calcular_descuento(venta)
        return Dinero(total.monto - descuento.monto, total.moneda)
