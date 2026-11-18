from __future__ import annotations


class Cantidad:
    """
    Value Object: Cantidad.

    Representa cuántos tickets se desean comprar.
    Regla R3: la cantidad debe ser mayor que cero y no exceder el máximo
    de tickets por compra.
    """

    MAXIMO_POR_COMPRA = 10

    def __init__(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError(f"La cantidad debe ser un entero positivo, recibido: {valor}")
        if valor > self.MAXIMO_POR_COMPRA:
            raise ValueError(
                f"La cantidad ({valor}) excede el máximo permitido por compra ({self.MAXIMO_POR_COMPRA})."
            )
        self._valor = valor

    @property
    def valor(self) -> int:
        return self._valor

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cantidad):
            return False
        return self._valor == otro._valor

    def __hash__(self) -> int:
        return hash(self._valor)

    def __repr__(self) -> str:
        return f"Cantidad({self._valor})"

    def __str__(self) -> str:
        return str(self._valor)
