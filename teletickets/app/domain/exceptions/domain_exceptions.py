class ErrorDominio(Exception):
    """Excepción base de los errores del dominio Teletickets."""


class EventoNoDisponibleError(ErrorDominio):
    """R2: No se puede vender tickets de un evento inactivo o ya realizado."""

    def __init__(self, nombre_evento: str):
        super().__init__(f"El evento '{nombre_evento}' no está disponible para la venta.")


class StockInsuficienteError(ErrorDominio):
    """R4: No se pueden vender más tickets que la capacidad disponible del evento."""

    def __init__(self, nombre_evento: str, solicitada: int, disponible: int):
        super().__init__(
            f"Stock insuficiente para el evento '{nombre_evento}': "
            f"se solicitaron {solicitada} tickets pero solo hay {disponible} disponibles."
        )


class VentaVaciaError(ErrorDominio):
    """Una venta no puede confirmarse sin líneas de ticket."""

    def __init__(self):
        super().__init__("No se puede confirmar una venta sin tickets.")


class VentaYaConfirmadaError(ErrorDominio):
    """R6: Una venta confirmada es inmutable; no se le pueden agregar tickets."""

    def __init__(self, venta_id: str):
        super().__init__(f"La venta '{venta_id}' ya está confirmada y no admite modificaciones.")


class TicketNoEncontradoError(ErrorDominio):
    def __init__(self, ticket_id: str):
        super().__init__(f"El ticket '{ticket_id}' no existe.")


class ClienteInvalidoError(ErrorDominio):
    def __init__(self, campo: str):
        super().__init__(f"El campo '{campo}' del cliente no puede estar vacío.")
