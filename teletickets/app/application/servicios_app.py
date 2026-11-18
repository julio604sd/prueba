from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from app.application.dtos.dtos import (
    ClienteDTO,
    CrearEventoDTO,
    EventoDTO,
    LineaVentaDTO,
    VentaDTO,
)
from app.domain.aggregates.venta import Venta
from app.domain.entities.cliente import Cliente
from app.domain.entities.evento import Evento
from app.domain.repositories.repositorios import (
    ClienteRepositorio,
    EventoRepositorio,
    TicketRepositorio,
    VentaRepositorio,
)
from app.domain.services.servicio_descuento import ServicioDescuento
from app.domain.value_objects.cantidad import Cantidad
from app.domain.value_objects.dinero import Dinero
from app.domain.value_objects.email import Email


class TeleticketsAppService:
    """
    Servicio de Aplicación (Capa Application).

    Orquesta el caso de uso "vender tickets": coordina agregados, servicios
    de dominio y repositorios, y traduce entidades internas a DTOs para no
    exponer el modelo de dominio hacia afuera.
    """

    def __init__(
        self,
        repo_eventos: EventoRepositorio,
        repo_clientes: ClienteRepositorio,
        repo_ventas: VentaRepositorio,
        repo_tickets: TicketRepositorio,
    ):
        self._repo_eventos = repo_eventos
        self._repo_clientes = repo_clientes
        self._repo_ventas = repo_ventas
        self._repo_tickets = repo_tickets
        self._servicio_descuento = ServicioDescuento()

    # ---------- Consultas ----------

    def listar_eventos_activos(self) -> list[EventoDTO]:
        return [self._to_evento_dto(e) for e in self._repo_eventos.get_activos()]

    def buscar_cliente_por_email(self, email: str) -> ClienteDTO | None:
        cliente = self._repo_clientes.get_por_email(email)
        return self._to_cliente_dto(cliente) if cliente else None

    # ---------- Casos de uso ----------

    def registrar_evento(self, dto: CrearEventoDTO) -> EventoDTO:
        evento = Evento(
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            categoria=dto.categoria,
            fecha_inicio=datetime.fromisoformat(dto.fecha_inicio),
            ubicacion=dto.ubicacion,
            precio_ticket=Dinero(Decimal(str(dto.precio))),
            capacidad_total=dto.capacidad_total,
        )
        self._repo_eventos.save(evento)
        return self._to_evento_dto(evento)

    def registrar_cliente(self, nombre: str, apellido: str, email: str) -> ClienteDTO:
        cliente = Cliente(nombre=nombre, apellido=apellido, email=Email(email))
        self._repo_clientes.save(cliente)
        return self._to_cliente_dto(cliente)

    def crear_venta(self, cliente_email: str) -> VentaDTO:
        cliente = self._repo_clientes.get_por_email(cliente_email)
        if cliente is None:
            raise ValueError(f"No existe un cliente con email '{cliente_email}'. Regístrelo primero.")
        venta = Venta(cliente=cliente)
        self._repo_ventas.save(venta)
        return self._to_venta_dto(venta)

    def agregar_tickets(self, venta_id: str, evento_id: str, cantidad: int) -> VentaDTO:
        venta = self._obtener_venta(venta_id)
        evento = self._repo_eventos.get_by_id(evento_id)
        if evento is None:
            raise ValueError(f"El evento '{evento_id}' no existe.")
        venta.agregar_evento(evento, Cantidad(cantidad))   # pasa por la raíz del agregado
        self._repo_ventas.save(venta)
        return self._to_venta_dto(venta)

    def confirmar_venta(self, venta_id: str) -> VentaDTO:
        venta = self._obtener_venta(venta_id)
        tickets = venta.confirmar()                        # R4 + emisión dentro del agregado
        for t in tickets:
            self._repo_tickets.save(t)
        for linea in venta.lineas:
            self._repo_eventos.save(linea.evento)
        self._repo_ventas.save(venta)
        return self._to_venta_dto(venta)

    # ---------- Helpers de mapeo Entidad -> DTO ----------

    def _obtener_venta(self, venta_id: str) -> Venta:
        venta = self._repo_ventas.get_by_id(venta_id)
        if venta is None:
            raise ValueError(f"La venta '{venta_id}' no existe.")
        return venta

    @staticmethod
    def _to_evento_dto(e: Evento) -> EventoDTO:
        return EventoDTO(
            evento_id=e.evento_id,
            nombre=e.nombre,
            categoria=e.categoria,
            fecha_inicio=e.fecha_inicio.isoformat(),
            ubicacion=e.ubicacion,
            precio=str(e.precio_ticket),
            disponibles=e.disponible,
            activo=e.activo,
        )

    @staticmethod
    def _to_cliente_dto(c: Cliente) -> ClienteDTO:
        return ClienteDTO(
            cliente_id=c.cliente_id,
            nombre_completo=c.nombre_completo,
            email=str(c.email),
            direccion=str(c.direccion) if c.direccion else "",
        )

    def _to_venta_dto(self, v: Venta) -> VentaDTO:
        descuento = self._servicio_descuento.calcular_descuento(v)
        total_final = self._servicio_descuento.aplicar_descuento(v)
        return VentaDTO(
            venta_id=v.venta_id,
            cliente=v.cliente.nombre_completo,
            lineas=tuple(
                LineaVentaDTO(l.evento.nombre, l.cantidad.valor, str(l.subtotal))
                for l in v.lineas
            ),
            total_tickets=v.total_tickets,
            total=str(v.total) if v.lineas else "S/ 0.00",
            descuento=str(descuento),
            total_final=str(total_final),
            estado=v.estado.value,
            tickets=tuple(t.codigo for t in v.tickets_emitidos),
        )
