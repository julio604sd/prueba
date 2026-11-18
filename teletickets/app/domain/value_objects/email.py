from __future__ import annotations


class Email:
    """
    Value Object: Email.

    Describe una dirección de correo electrónico del dominio.
    Es inmutable y se compara por valor (no tiene ID propia).
    """

    def __init__(self, direccion: str):
        if not direccion or "@" not in direccion or "." not in direccion.split("@")[-1]:
            raise ValueError(f"Email inválido: '{direccion}'")
        self._direccion = direccion.strip().lower()

    @property
    def direccion(self) -> str:
        return self._direccion

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Email):
            return False
        return self._direccion == otro._direccion

    def __hash__(self) -> int:
        return hash(self._direccion)

    def __repr__(self) -> str:
        return f"Email('{self._direccion}')"

    def __str__(self) -> str:
        return self._direccion
