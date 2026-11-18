"""
Capa Presentación: controlador + esquema de salida para la consola.

El controlador NO conoce entidades del dominio: solo habla con el
servicio de aplicación y recibe/entrega DTOs.
"""

from app.application.dtos.dtos import CrearEventoDTO, EventoDTO, VentaDTO
from app.application.servicios_app import TeleticketsAppService


class EsquemaConsola:
    """Formatea los DTOs para mostrarlos al usuario (schema de presentación)."""

    @staticmethod
    def evento(e: EventoDTO) -> str:
        estado = "ACTIVO" if e.activo else "INACTIVO"
        return (
            f"  [{e.evento_id[:8]}] {e.nombre} | {e.categoria} | {e.fecha_inicio} | "
            f"{e.ubicacion} | Precio: {e.precio} | Disponibles: {e.disponibles} | {estado}"
        )

    @staticmethod
    def venta(v: VentaDTO) -> str:
        lineas = "\n".join(
            f"     - {l.evento_nombre}: {l.cantidad} ticket(s) x subtotal {l.subtotal}"
            for l in v.lineas
        ) or "     (sin tickets)"
        tickets = ", ".join(v.tickets) if v.tickets else "-"
        return (
            f"\n     VENTA {v.venta_id[:8]} | Cliente: {v.cliente} | Estado: {v.estado}\n"
            f"     Detalle:\n{lineas}\n"
            f"     Total tickets: {v.total_tickets} | Subtotal: {v.total} | "
            f"Descuento: {v.descuento} | TOTAL A PAGAR: {v.total_final}\n"
            f"     Tickets emitidos: {tickets}"
        )


class TeleticketsController:
    """Controlador de la demo: expone las acciones que verá el usuario."""

    def __init__(self, servicio: TeleticketsAppService):
        self._servicio = servicio
        self._esquema = EsquemaConsola()

    def ver_eventos(self) -> None:
        print("\n=== EVENTOS DISPONIBLES (Teletickets) ===")
        for e in self._servicio.listar_eventos_activos():
            print(self._esquema.evento(e))

    def nuevo_evento(self) -> None:
        dto = CrearEventoDTO(
            nombre="Festival Electrónica 2026",
            descripcion="DJ set internacional",
            categoria="Concierto",
            fecha_inicio="2027-01-10T22:00",
            ubicacion="Costa Verde, Lima",
            precio=90,
            capacidad_total=800,
        )
        e = self._servicio.registrar_evento(dto)
        print(f"\nEvento registrado: {self._esquema.evento(e)}")

    def flujo_compra_demo(self) -> None:
        """Caso de uso completo: crear venta -> agregar tickets -> confirmar."""
        eventos = self._servicio.listar_eventos_activos()
        ev1, ev2 = eventos[0], eventos[1]

        venta = self._servicio.crear_venta("ana.torres@gmail.com")
        print(self._esquema.venta(venta))

        venta = self._servicio.agregar_tickets(venta.venta_id, ev1.evento_id, 3)
        print(self._esquema.venta(venta))

        venta = self._servicio.agregar_tickets(venta.venta_id, ev2.evento_id, 2)
        print(self._esquema.venta(venta))   # 5 tickets -> aplica descuento D1 (10%)

        venta = self._servicio.confirmar_venta(venta.venta_id)
        print(self._esquema.venta(venta))

    def flujo_compra_vip(self) -> None:
        """Cliente VIP acumulando descuentos D1 + D2."""
        eventos = self._servicio.listar_eventos_activos()
        ev = eventos[0]

        venta = self._servicio.crear_venta("carlos@vip.teletickets.pe")
        venta = self._servicio.agregar_tickets(venta.venta_id, ev.evento_id, 6)
        venta = self._servicio.confirmar_venta(venta.venta_id)
        print(self._esquema.venta(venta))
