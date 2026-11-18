"""
Punto de entrada de la demostración Teletickets (arquitectura DDD, 4 capas).

Ejecutar desde la carpeta teletickets/:
    python ejecutar.py
"""

from app.infrastructure.base_datos import BaseDeDatosSimulada
from app.infrastructure.repositories.repositorios_memoria import (
    ClienteRepositorioMemoria,
    EventoRepositorioMemoria,
    TicketRepositorioMemoria,
    VentaRepositorioMemoria,
)
from app.application.servicios_app import TeleticketsAppService
from app.presentation.controlador import TeleticketsController


def construir_dependencias() -> TeleticketsController:
    """Composición raíz: se inyectan las implementaciones concretas."""
    db = BaseDeDatosSimulada.obtener()
    servicio = TeleticketsAppService(
        repo_eventos=EventoRepositorioMemoria(db),
        repo_clientes=ClienteRepositorioMemoria(db),
        repo_ventas=VentaRepositorioMemoria(db),
        repo_tickets=TicketRepositorioMemoria(db),
    )
    return TeleticketsController(servicio)


def main() -> None:
    controller = construir_dependencias()

    print("=" * 70)
    print("  TELETTICKETS - Demostración DDD en Python (4 capas)")
    print("=" * 70)

    # 1. Catálogo de eventos (Value Object Dinero en precios)
    controller.ver_eventos()

    # 2. Registro de un nuevo evento (Aggregate Root Evento)
    controller.nuevo_evento()

    # 3. Caso de uso: compra normal con descuento por volumen (D1)
    print("\n=== FLUJO DE COMPRA NORMAL (agregado Venta como Aggregate Root) ===")
    controller.flujo_compra_demo()

    # 4. Caso de uso: cliente VIP (Domain Service ServicioDescuento, D1+D2)
    print("\n=== FLUJO DE COMPRA CLIENTE VIP (ServicioDescuento D1+D2) ===")
    controller.flujo_compra_vip()

    # 5. Verificación de reglas de negocio que FALLAN (invariantes custodiadas)
    print("\n=== REGLAS DE NEGOCIO PROTEGIDAS POR EL DOMINIO ===")
    from app.domain.value_objects.dinero import Dinero
    from app.domain.value_objects.cantidad import Cantidad
    from app.domain.exceptions.domain_exceptions import EventoNoDisponibleError

    try:
        Dinero(-10)                       # R1: precio negativo
    except ValueError as ex:
        print(f"  [R1] Precio inválido rechazado .......: {ex}")

    try:
        Cantidad(11)                      # R3: máximo 10 tickets por línea
    except ValueError as ex:
        print(f"  [R3] Cantidad excesiva rechazada ....: {ex}")

    eventos = controller._servicio.listar_eventos_activos()
    from app.application.servicios_app import TeleticketsAppService  # noqa: F401
    db = BaseDeDatosSimulada.obtener()
    evento = list(db.eventos.values())[0]
    evento.desactivar()
    try:
        cliente = list(db.clientes.values())[0]
        from app.domain.aggregates.venta import Venta
        v = Venta(cliente)
        v.agregar_evento(evento, Cantidad(1))   # R2: evento inactivo
    except EventoNoDisponibleError as ex:
        print(f"  [R2] Evento inactivo bloqueado ......: {ex}")
    evento.activar()  # restaurar

    print("\nDemostración finalizada.")


if __name__ == "__main__":
    main()
