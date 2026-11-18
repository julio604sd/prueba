from dataclasses import dataclass, field


@dataclass(frozen=True)
class EventoDTO:
    """DTO de salida: expone un Evento SIN revelar la entidad del dominio."""
    evento_id: str
    nombre: str
    categoria: str
    fecha_inicio: str
    ubicacion: str
    precio: str          # formateado, ej. "S/ 80.00"
    disponibles: int
    activo: bool


@dataclass(frozen=True)
class ClienteDTO:
    cliente_id: str
    nombre_completo: str
    email: str
    direccion: str = ""


@dataclass(frozen=True)
class LineaVentaDTO:
    evento_nombre: str
    cantidad: int
    subtotal: str


@dataclass(frozen=True)
class VentaDTO:
    venta_id: str
    cliente: str
    lineas: tuple[LineaVentaDTO, ...] = ()
    total_tickets: int = 0
    total: str = ""
    descuento: str = ""
    total_final: str = ""
    estado: str = ""
    tickets: tuple[str, ...] = ()   # códigos de tickets emitidos


@dataclass(frozen=True)
class CrearEventoDTO:
    """DTO de entrada para registrar un evento (capa presentación -> aplicación)."""
    nombre: str
    descripcion: str
    categoria: str
    fecha_inicio: str      # ISO: "2026-12-01T20:00"
    ubicacion: str
    precio: float
    capacidad_total: int
