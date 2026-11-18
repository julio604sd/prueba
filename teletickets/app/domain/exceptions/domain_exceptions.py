"""Excepciones simples de las reglas del dominio Teletickets."""


class EventoNoDisponibleError(Exception):
    """R2: no se venden tickets de eventos inactivos."""


class StockInsuficienteError(Exception):
    """R4: no se pueden vender mas tickets que los disponibles."""
