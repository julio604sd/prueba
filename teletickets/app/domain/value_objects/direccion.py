from __future__ import annotations


class DireccionInvalidaError(ValueError):
    def __init__(self, campo: str):
        super().__init__(f"El campo '{campo}' de la dirección no puede estar vacío.")


class Direccion:
    """
    Value Object: Dirección.

    Agrupa los campos de una dirección postal. Se trata como un todo:
    si cualquier campo cambia, es una dirección DIFERENTE (inmutabilidad).
    """

    def __init__(self, calle: str, ciudad: str, departamento: str, codigo_postal: str):
        self._calle = self._validar_campo(calle, "calle")
        self._ciudad = self._validar_campo(ciudad, "ciudad")
        self._departamento = self._validar_campo(departamento, "departamento")
        self._codigo_postal = self._validar_campo(codigo_postal, "codigo_postal")

    @staticmethod
    def _validar_campo(valor: str, nombre: str) -> str:
        if not valor or not valor.strip():
            raise DireccionInvalidaError(nombre)
        return valor.strip()

    @property
    def calle(self) -> str:
        return self._calle

    @property
    def ciudad(self) -> str:
        return self._ciudad

    @property
    def departamento(self) -> str:
        return self._departamento

    @property
    def codigo_postal(self) -> str:
        return self._codigo_postal

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Direccion):
            return False
        return (
            self._calle == otro._calle
            and self._ciudad == otro._ciudad
            and self._departamento == otro._departamento
            and self._codigo_postal == otro._codigo_postal
        )

    def __hash__(self) -> int:
        return hash((self._calle, self._ciudad, self._departamento, self._codigo_postal))

    def __repr__(self) -> str:
        return (
            f"Direccion(calle='{self._calle}', ciudad='{self._ciudad}', "
            f"departamento='{self._departamento}', cp='{self._codigo_postal}')"
        )

    def __str__(self) -> str:
        return f"{self._calle}, {self._ciudad}, {self._departamento} {self._codigo_postal}"
