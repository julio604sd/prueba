# 🎟️ Teletickets — Arquitectura DDD en Python (4 capas)

Solución al caso de negocio **Teletickets** (venta y gestión de tickets a eventos),
siguiendo la demostración de la tienda en línea vista en clase.

## Estructura de carpetas

```
teletickets/
├── ejecutar.py                      # Punto de entrada de la demo
└── app/
    ├── domain/                      # ⭐ CAPA DE DOMINIO (enfoque principal)
    │   ├── entities/                # Entidades (ID única, estado mutable)
    │   │   ├── cliente.py           # Cliente (cliente_id, VO Email/Direccion)
    │   │   ├── evento.py            # Evento = "Producto" (precio VO Dinero, stock, activo)
    │   │   └── ticket.py            # Ticket (código único, ciclo emitido→validado/anulado)
    │   ├── value_objects/           # Value Objects (inmutables, sin ID, igualdad por valor)
    │   │   ├── dinero.py            # Dinero (monto + moneda, R1: no negativo, sumar/multiplicar)
    │   │   ├── email.py             # Email (valida formato)
    │   │   ├── direccion.py         # Dirección (calle, ciudad, departamento, CP)
    │   │   └── cantidad.py          # Cantidad (R3: 1..10 tickets por compra)
    │   ├── aggregates/              # Agregados / Aggregate Root
    │   │   ├── venta.py             # Venta (raíz: custodia líneas, calcula total, confirma)
    │   │   └── linea_venta.py       # LineaVenta (componente interno con identidad local)
    │   ├── services/
    │   │   └── servicio_descuento.py# Domain Service: ServicioDescuento (D1 volumen, D2 VIP)
    │   ├── repositories/
    │   │   └── repositorios.py      # Interfaces abstractas (get_by_id/get_all/save/delete)
    │   └── exceptions/
    │       └── domain_exceptions.py # Excepciones de reglas de negocio
    ├── application/                 # CAPA DE APLICACIÓN
    │   ├── dtos/dtos.py             # DTOs (dataclasses frozen, mapeo entre capas)
    │   └── servicios_app.py         # TeleticketsAppService (orquesta casos de uso)
    ├── infrastructure/              # CAPA DE INFRAESTRUCTURA
    │   ├── base_datos.py            # Simulación de BD en memoria + datos seed
    │   └── repositories/repositorios_memoria.py  # Implementaciones concretas
    └── presentation/                # CAPA DE PRESENTACIÓN
        └── controlador.py           # Controlador + esquema de consola (solo ve DTOs)
```

## Reglas de negocio modeladas (Lenguaje Ubicuo)

| Regla | Dónde se aplica |
|-------|-----------------|
| R1: El precio no puede ser negativo | VO `Dinero` |
| R2: Solo se venden tickets de eventos activos | Entidad `Evento.verificar_disponibilidad()` |
| R3: Máximo 10 tickets por línea de compra | VO `Cantidad` |
| R4: No vender más tickets que la capacidad disponible | `Evento.reducir_stock()` |
| R5: El total se deriva siempre de las líneas | Aggregate Root `Venta.total` |
| R6: Venta confirmada no se modifica | `Venta._verificar_editable()` |
| D1: ≥5 tickets → 10% descuento | Domain Service `ServicioDescuento` |
| D2: Cliente VIP → +15% acumulable | Domain Service `ServicioDescuento` |

## Cómo ejecutar

```bash
cd teletickets
python ejecutar.py
```

La demo muestra: catálogo de eventos, registro de un nuevo evento, una compra
normal (con descuento por volumen), una compra VIP (descuentos acumulados),
tickets emitidos con código único, y las reglas R1/R2/R3 rechazando intentos
inválidos.
