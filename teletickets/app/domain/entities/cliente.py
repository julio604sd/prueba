from __future__ import annotations

import uuid

from app.domain.value_objects.email import Email


class Cliente:
    """
    Entidad: Cliente.

    Posee un identificador único (cliente_id) que mantiene a lo largo del
    tiempo aunque cambien sus atributos. Su dato de contacto es un
    Value Object (Email).
    """

    def __init__(
        self,
        nombre: str,
        apellido: str,
        email: Email,
        cliente_id: str | None = None,
    ):
        self._cliente_id = cliente_id or str(uuid.uuid4())
        self._nombre = self._validar(nombre, "nombre")
        self._apellido = self._validar(apellido, "apellido")
        # VO: garantiza un correo válido e inmutable
        self._email = email

    @staticmethod
    def _validar(valor: str, campo: str) -> str:
        if not valor or not valor.strip():
            raise ValueError(f"El campo '{campo}' del cliente no puede estar vacío.")
        return valor.strip()

    # ---- Propiedades de solo lectura ----

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def email(self) -> Email:
        return self._email

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    # ---- Comportamientos del dominio (mutabilidad con identidad estable) ----

    def actualizar_email(self, nuevo_email: Email) -> None:
        """El cliente cambia de correo: sigue siendo el MISMO cliente (misma ID)."""
        self._email = nuevo_email

    # Dos clientes son el mismo si comparten la identidad
    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cliente):
            return False
        return self._cliente_id == otro._cliente_id

    def __hash__(self) -> int:
        return hash(self._cliente_id)

    def __repr__(self) -> str:
        return f"Cliente(id='{self._cliente_id}', nombre='{self.nombre_completo}', email={self._email})"
