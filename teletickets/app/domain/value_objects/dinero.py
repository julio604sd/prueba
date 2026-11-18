from __future__ import annotations

from decimal import Decimal


class Dinero:
    """
    Value Object: Dinero.

    Representa un valor monetario con monto y moneda.
    Es INMUTABLE: las operaciones (sumar, multiplicar) devuelven
    un NUEVO objeto Dinero, nunca modifican la instancia original.

    Regla R1: el monto no puede ser negativo.
    """

    def __init__(self, monto: Decimal | float | str, moneda: str = "PEN"):
        # Regla R1: monto no puede ser negativo
        monto_dec = Decimal(str(monto))
        if monto_dec < Decimal("0"):
            raise ValueError(f"El monto no puede ser negativo: {monto_dec}")
        if not moneda or not moneda.strip():
            raise ValueError("La moneda no puede estar vacía.")

        # Almacenamos como Decimal para evitar errores de punto flotante
        self._monto = monto_dec
        self._moneda = moneda.upper().strip()

    @property
    def monto(self) -> Decimal:
        return self._monto

    @property
    def moneda(self) -> str:
        return self._moneda

    def _validar_misma_moneda(self, otro: "Dinero") -> None:
        if self._moneda != otro._moneda:
            raise ValueError(
                f"No se pueden operar montos de monedas distintas: "
                f"{self._moneda} vs {otro._moneda}"
            )

    def sumar(self, otro: "Dinero") -> "Dinero":
        """Retorna un NUEVO objeto Dinero con la suma (inmutabilidad)."""
        self._validar_misma_moneda(otro)
        return Dinero(self._monto + otro._monto, self._moneda)

    def multiplicar(self, factor: int) -> "Dinero":
        """Retorna un NUEVO objeto Dinero multiplicado por un factor entero."""
        if factor < 0:
            raise ValueError("El factor no puede ser negativo.")
        return Dinero(self._monto * Decimal(factor), self._moneda)

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Dinero):
            return False
        return self._monto == otro._monto and self._moneda == otro._moneda

    def __hash__(self) -> int:
        return hash((self._monto, self._moneda))

    def __repr__(self) -> str:
        return f"Dinero(monto={self._monto}, moneda='{self._moneda}')"

    def __str__(self) -> str:
        return f"S/ {self._monto:.2f}" if self._moneda == "PEN" else f"{self._monto:.2f} {self._moneda}"
