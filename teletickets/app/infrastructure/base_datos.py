"""
Capa Infraestructura: simulación de base de datos.

Un "diccionario en memoria" que hace las veces de BD para la demo.
En producción se reemplazaría por SQLAlchemy, PostgreSQL, etc., sin
tocar la capa de Dominio (gracias a los interfaces de Repositorio).
"""

from app.domain.entities.cliente import Cliente
from app.domain.entities.evento import Evento
from app.domain.entities.ticket import Ticket
from app.domain.aggregates.venta import Venta
from app.domain.value_objects.direccion import Direccion
from app.domain.value_objects.dinero import Dinero
from app.domain.value_objects.email import Email
from app.domain.value_objects.cantidad import Cantidad  # noqa: F401

from datetime import datetime


class BaseDeDatosSimulada:
    """Base de datos en memoria (singletons por ejecución de la demo)."""

    _instancias: dict[str, "BaseDeDatosSimulada"] = {}

    def __init__(self):
        self.eventos: dict[str, Evento] = {}
        self.clientes: dict[str, Cliente] = {}
        self.ventas: dict[str, Venta] = {}
        self.tickets: dict[str, Ticket] = {}

    @classmethod
    def obtener(cls) -> "BaseDeDatosSimulada":
        if "db" not in cls._instancias:
            db = cls()
            db._cargar_datos_iniciales()
            cls._instancias["db"] = db
        return cls._instancias["db"]

    def _cargar_datos_iniciales(self):
        """Datos de ejemplo (seed) del negocio Teletickets."""
        eventos_seed = [
            Evento("Lima Rock Fest 2026", "Concierto de rock en vivo",
                   "Concierto", datetime(2026, 12, 5, 20, 0),
                   "Estadio Nacional, Lima", Dinero(80), 500),
            Evento("Teletickets Comedy Night", "Stand-up con comediantes invitados",
                   "Comedia", datetime(2026, 12, 12, 21, 0),
                   "Teatro Municipal, Lima", Dinero(45), 200),
            Evento("Final Liga 1", "Partido de fútbol - final nacional",
                   "Deporte", datetime(2026, 12, 20, 15, 30),
                   "Arena Esports Park", Dinero(60), 300),
            Evento("Expo Tecnología 2026", "Feria de tecnología e IA",
                   "Feria", datetime(2026, 12, 28, 10, 0),
                   "Jockey Club, Lima", Dinero(25), 1000),
        ]
        for e in eventos_seed:
            self.eventos[e.evento_id] = e

        clientes_seed = [
            Cliente("Ana", "Torres", Email("ana.torres@gmail.com"),
                    Direccion("Av. Larco 123", "Lima", "Lima", "15046")),
            Cliente("Carlos", "Vip", Email("carlos@vip.teletickets.pe")),
        ]
        for c in clientes_seed:
            self.clientes[c.cliente_id] = c
