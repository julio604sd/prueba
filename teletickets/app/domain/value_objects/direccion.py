from __future__ import annotations


class Direccion:
    """
    Value Object: Direccion.

    Agrupa los campos de una direccion postal. Es inmutable y sin ID:
    si cualquier campo cambia, es una direccion diferente.
    """

    def __init__(self, calle: str, ciudad: str):
        if not calle or not calle.strip() or not ciudad or not ciudad.strip():
            raise ValueError("La direccion requiere calle y ciudad.")
        self._calle = calle.strip()
        self._ciudad = ciudad.strip()

    @property
    def calle(self) -> str:
        return self._calle

    @property
    def ciudad(self) -> str:
        return self._ciudad

    def __eq__(self, otro: object) -> bool:
        return isinstance(otro, Direccion) and (self._calle, self._ciudad) == (otro._calle, otro._ciudad)

    def __hash__(self) -> int:
        return hash((self._calle, self._ciudad))

    def __str__(self) -> str:
        return f"{self._calle}, {self._ciudad}"
